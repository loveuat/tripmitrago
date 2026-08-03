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


def build_location(row: dict):
    name = (row.get("name") or "").strip()
    if not name:
        return None
    district = (row.get("district") or "").strip() or None
    sub_district = (row.get("sub_district") or "").strip() or None
    pincode = (row.get("pincode") or "").strip() or None
    slug = slugify(name, sub_district, district, pincode)
    return Location(
        name=name,
        type=(row.get("type") or "village").strip(),
        state=(row.get("state") or "").strip(),
        district=district,
        sub_district=sub_district,
        latitude=to_float(row.get("latitude")),
        longitude=to_float(row.get("longitude")),
        country=(row.get("country") or "India").strip(),
        block=sub_district,
        pincode=pincode,
        slug=slug,
        is_serviceable=to_bool(row.get("is_serviceable", "false")),
        priority=to_int(row.get("priority"), 0),
    )


@router.post("/location-import", name="location_import")
async def import_csv(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))

    inserted, skipped, errors = 0, 0, []
    for i, row in enumerate(reader, start=2):
        try:
            loc = build_location(row)
            if loc is None:
                skipped += 1
                continue
            if db.query(Location).filter_by(slug=loc.slug).first():
                skipped += 1
                continue
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