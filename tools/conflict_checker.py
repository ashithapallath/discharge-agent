def detect_conflicts(extracted_data):
    """
    Lightweight rule-based conflict detector (no OpenAI dependency)
    """

    if isinstance(extracted_data, list):
        extracted_data = extracted_data[0] if extracted_data else {}

    conflicts = []

    if not isinstance(extracted_data, dict):
        return []

    diagnosis = extracted_data.get("principal_diagnosis", "")
    course = extracted_data.get("hospital_course", "")
    condition = extracted_data.get("discharge_condition", "")

    # Simple rule-based checks
    if diagnosis == "MISSING":
        conflicts.append("Missing principal diagnosis")

    if course == "MISSING":
        conflicts.append("Missing hospital course")

    if condition == "MISSING":
        conflicts.append("Missing discharge condition")

    # Optional heuristic
    if diagnosis and condition and diagnosis.lower() in condition.lower():
        conflicts.append("Possible redundancy between diagnosis and condition")

    return conflicts