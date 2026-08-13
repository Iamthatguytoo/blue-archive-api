from datetime import timezone

def serialize_student(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)
    if "class" in doc:
        doc["class_name"] = doc.pop("class")
    return doc

def serialize_banner(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)

    return doc

def normalize_banner_timezone(banner):
    banner = banner.copy()

    for field in ("start_date", "end_date"):
        dt = banner[field]

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        banner[field] = dt

    return banner