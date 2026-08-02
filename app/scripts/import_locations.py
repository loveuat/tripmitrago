import csv

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.location import Location

db: Session = SessionLocal()

BATCH_SIZE = 5000

objects = []

with open("data/villages.csv", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        objects.append(
            Location(
                name=row["village_name"],
                type=row["location_type"],
                state=row["state"],
                district=row["district"],
                sub_district=row["sub_district"],
                pincode=row["pincode"],
                latitude=float(row["latitude"]) if row["latitude"] else None,
                longitude=float(row["longitude"]) if row["longitude"] else None,
                population=int(row["population"]) if row["population"] else None,
                is_serviceable=row["is_serviceable"].lower() == "true",
                priority=int(row["priority"]) if row["priority"] else 0,
            )
        )

        if len(objects) >= BATCH_SIZE:
            db.bulk_save_objects(objects)
            db.commit()
            objects = []

if objects:
    db.bulk_save_objects(objects)
    db.commit()

db.close()

print("Import completed.")