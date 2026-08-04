import csv
import io
import re
from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.location import Location

router = APIRouter()


def slugify(*parts: str) -> str:
    text = "-".join(p for p in parts if p).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def to_bool(v): return str(v).strip().lower() in ("true", "1", "yes", "t")
def to_float(v):
    try: return float(v) if v else None
    except: return None
def to_int(v, d=0):
    try: return int(v) if v else d
    except: return d


def build_location(row: dict, slug: str):
    return Location(
        name=(row.get("name") or "").strip(),
        name_hi=(row.get("name_hi") or "").strip() or None,
        type=(row.get("type") or "village").strip(),
        country=(row.get("country") or "India").strip(),
        country_hi=(row.get("country_hi") or "").strip() or None,
        state=(row.get("state") or "").strip(),
        state_hi=(row.get("state_hi") or "").strip() or None,
        district=(row.get("district") or "").strip() or None,
        district_hi=(row.get("district_hi") or "").strip() or None,
        sub_district=(row.get("sub_district") or "").strip() or None,
        sub_district_hi=(row.get("sub_district_hi") or "").strip() or None,
        block=(row.get("sub_district") or "").strip() or None,
        block_hi=(row.get("block_hi") or "").strip() or None,
        panchayat=(row.get("panchayat") or "").strip() or None,
        panchayat_hi=(row.get("panchayat_hi") or "").strip() or None,
        pincode=(row.get("pincode") or "").strip() or None,
        latitude=to_float(row.get("latitude")),
        longitude=to_float(row.get("longitude")),
        slug=slug,
        is_serviceable=to_bool(row.get("is_serviceable", "false")),
        priority=to_int(row.get("priority"), 0),
        airport_code=(row.get("airport_code") or "").strip() or None,
        railway_station_code=(row.get("railway_station_code") or "").strip() or None,
        seo_title=(row.get("seo_title") or "").strip() or None,
        seo_title_hi=(row.get("seo_title_hi") or "").strip() or None,
        seo_description=(row.get("seo_description") or "").strip() or None,
        seo_description_hi=(row.get("seo_description_hi") or "").strip() or None,
        keywords=(row.get("keywords") or "").strip() or None,
        keywords_hi=(row.get("keywords_hi") or "").strip() or None,
        content=(row.get("content") or "").strip() or None,
        content_hi=(row.get("content_hi") or "").strip() or None,
        banner_image=(row.get("banner_image") or "").strip() or None,
        thumbnail_image=(row.get("thumbnail_image") or "").strip() or None,
        is_active=to_bool(row.get("is_active", "true")),
        is_featured=to_bool(row.get("is_featured", "false")),
    )


@router.post("/location-import", name="location_import")
async def import_csv(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))

    # Pre-load existing slugs once, to avoid a DB query per row
    existing_slugs = set(s for (s,) in db.query(Location.slug).all())
    used_in_batch = set()

    inserted, skipped, errors = 0, 0, []

    for i, row in enumerate(reader, start=2):
        try:
            name = (row.get("name") or "").strip()
            if not name:
                skipped += 1
                continue

            district = (row.get("district") or "").strip() or None
            sub_district = (row.get("sub_district") or "").strip() or None
            pincode = (row.get("pincode") or "").strip() or None

            base_slug = slugify(name, sub_district, district, pincode)
            slug = base_slug
            suffix = 2
            # Keep appending -2, -3, ... until it's unique against DB and this batch
            while slug in existing_slugs or slug in used_in_batch:
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            used_in_batch.add(slug)

            loc = build_location(row, slug)
            db.add(loc)
            inserted += 1

        except Exception as e:
            errors.append(f"Row {i}: {e}")

    db.commit()

    redirect_url = str(request.url_for("admin:list", identity="location"))
    return RedirectResponse(
        url=f"{redirect_url}?imported={inserted}&skipped={skipped}",
        status_code=303,
    )