def create_evidence(
    value,
    document,
    page,
    evidence,
    confidence
):

    return {
        "value": value,
        "document": document,
        "page": page,
        "evidence": evidence,
        "confidence": confidence
    }