from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.schemas.location_detail import LocationDetail
from app.database import get_db
from app.models.location import Location
from app.schemas.location import LocationSearchItem

router = APIRouter(
    prefix="/api/v1/locations",
    tags=["Locations"]
)


def _score(value, q):
    if not value:
        return 0
    v = value.strip().lower()
    if not v:
        return 0
    if v == q:
        return 100
    if v.startswith(q):
        return 60
    if q in v:
        return 30
    return 0


@router.get(
    "/search",
    response_model=list[LocationSearchItem],
)
def search_locations(
    q: str = Query(..., min_length=2),
    lang: str = Query("en"),
    db: Session = Depends(get_db),
):
    raw_q = q.strip()
    ql = raw_q.lower()
    like = f"%{raw_q}%"

    rows = (
        db.query(Location)
        .filter(
            Location.is_active == True,
            or_(
                Location.name.ilike(like),
                Location.name_hi.ilike(like),
                Location.district.ilike(like),
                Location.district_hi.ilike(like),
                Location.sub_district.ilike(like),
                Location.sub_district_hi.ilike(like),
                Location.block.ilike(like),
                Location.block_hi.ilike(like),
                Location.state.ilike(like),
                Location.state_hi.ilike(like),
                Location.pincode.ilike(like),
            ),
        )
        .limit(500)
        .all()
    )

    name_results = []
    district_map = {}
    sub_district_map = {}
    block_map = {}
    state_map = {}
    pincode_map = {}

    def loc_field(row, field):
        hi_val = getattr(row, f"{field}_hi", None)
        return hi_val if (lang == "hi" and hi_val) else getattr(row, field, None)

    for row in rows:
        name_score = max(_score(row.name, ql), _score(row.name_hi, ql))
        district_score = max(_score(row.district, ql), _score(row.district_hi, ql))
        sub_district_score = max(_score(row.sub_district, ql), _score(row.sub_district_hi, ql))
        block_score = max(_score(row.block, ql), _score(row.block_hi, ql))
        state_score = max(_score(row.state, ql), _score(row.state_hi, ql))
        pincode_score = _score(row.pincode, ql)

        if name_score > 0:
            hierarchy = [h for h in [
                loc_field(row, "sub_district"),
                loc_field(row, "district"),
                loc_field(row, "state"),
            ] if h]
            name_results.append((
                name_score, row.priority,
                LocationSearchItem(
                    id=str(row.id),
                    type=row.type,
                    name=loc_field(row, "name"),
                    name_hi=row.name_hi,
                    hierarchy=hierarchy,
                    slug=row.slug,
                    pincode=row.pincode,
                    latitude=row.latitude,
                    longitude=row.longitude,
                    is_serviceable=row.is_serviceable,
                    priority=row.priority,
                ),
            ))

        if district_score > 0 and row.district:
            key = (row.district, row.state)
            if key not in district_map or district_score > district_map[key][0]:
                district_map[key] = (district_score, row)

        if sub_district_score > 0 and row.sub_district:
            key = (row.sub_district, row.district, row.state)
            if key not in sub_district_map or sub_district_score > sub_district_map[key][0]:
                sub_district_map[key] = (sub_district_score, row)

        if block_score > 0 and row.block and row.block != row.sub_district:
            key = (row.block, row.district, row.state)
            if key not in block_map or block_score > block_map[key][0]:
                block_map[key] = (block_score, row)

        if state_score > 0 and row.state:
            key = (row.state,)
            if key not in state_map or state_score > state_map[key][0]:
                state_map[key] = (state_score, row)

        if pincode_score > 0 and row.pincode:
            key = (row.pincode,)
            if key not in pincode_map:
                pincode_map[key] = [pincode_score, row, 1]
            else:
                pincode_map[key][2] += 1
                if pincode_score > pincode_map[key][0]:
                    pincode_map[key][0] = pincode_score

    aggregated = []

    for (district, state), (score, row) in district_map.items():
        aggregated.append((
            score, row.priority,
            LocationSearchItem(
                id=f"district-{district}-{state}",
                type="district",
                name=loc_field(row, "district"),
                hierarchy=[state] if state else [],
                latitude=row.latitude,
                longitude=row.longitude,
                is_serviceable=row.is_serviceable,
                priority=row.priority,
            ),
        ))

    for (sub_district, district, state), (score, row) in sub_district_map.items():
        aggregated.append((
            score, row.priority,
            LocationSearchItem(
                id=f"subdistrict-{sub_district}-{district}-{state}",
                type="sub_district",
                name=loc_field(row, "sub_district"),
                hierarchy=[h for h in [district, state] if h],
                latitude=row.latitude,
                longitude=row.longitude,
                is_serviceable=row.is_serviceable,
                priority=row.priority,
            ),
        ))

    for (block, district, state), (score, row) in block_map.items():
        aggregated.append((
            score, row.priority,
            LocationSearchItem(
                id=f"block-{block}-{district}-{state}",
                type="block",
                name=loc_field(row, "block"),
                hierarchy=[h for h in [district, state] if h],
                latitude=row.latitude,
                longitude=row.longitude,
                is_serviceable=row.is_serviceable,
                priority=row.priority,
            ),
        ))

    for (state,), (score, row) in state_map.items():
        aggregated.append((
            score, row.priority,
            LocationSearchItem(
                id=f"state-{state}",
                type="state",
                name=loc_field(row, "state"),
                hierarchy=[],
                latitude=row.latitude,
                longitude=row.longitude,
                is_serviceable=row.is_serviceable,
                priority=row.priority,
            ),
        ))

    for (pincode,), (score, row, count) in pincode_map.items():
        aggregated.append((
            score, row.priority,
            LocationSearchItem(
                id=f"pincode-{pincode}",
                type="pincode",
                name=pincode,
                hierarchy=[h for h in [
                    loc_field(row, "sub_district"),
                    loc_field(row, "district"),
                    loc_field(row, "state"),
                ] if h],
                pincode=pincode,
                latitude=row.latitude,
                longitude=row.longitude,
                is_serviceable=row.is_serviceable,
                priority=row.priority,
            ),
        ))

    combined = name_results + aggregated
    combined.sort(key=lambda item: (-item[0], -item[1], item[2].name.lower()))

    seen = set()
    final = []
    for _, _, item in combined:
        dedup_key = (item.type, item.name.lower(), tuple(item.hierarchy))
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        final.append(item)
        if len(final) >= 10:
            break

    return final


@router.get(
    "/{slug}",
    response_model=LocationDetail
)
def get_location(
    slug: str,
    lang: str = Query("en"),
    db: Session = Depends(get_db)
):
    location = (
        db.query(Location)
        .filter(
            Location.slug == slug,
            Location.is_active == True
        )
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )

    if lang == "hi":
        if location.name_hi:
            location.name = location.name_hi
        if location.country_hi:
            location.country = location.country_hi
        if location.state_hi:
            location.state = location.state_hi
        if location.district_hi:
            location.district = location.district_hi
        if location.sub_district_hi:
            location.sub_district = location.sub_district_hi
        if location.block_hi:
            location.block = location.block_hi
        if location.panchayat_hi:
            location.panchayat = location.panchayat_hi
        if location.seo_title_hi:
            location.seo_title = location.seo_title_hi
        if location.seo_description_hi:
            location.seo_description = location.seo_description_hi
        if location.keywords_hi:
            location.keywords = location.keywords_hi
        if location.content_hi:
            location.content = location.content_hi

    return location