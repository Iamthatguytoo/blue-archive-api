def serialize_student(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)
    if "class" in doc:
        doc["class_name"] = doc.pop("class")
    return doc
