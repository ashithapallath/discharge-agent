def classify_page(text):

    text_upper = text.upper()

    # =========================
    # DISCHARGE CHECKLIST
    # =========================

    if (
        "DISCHARGE CHECK LIST" in text_upper
        or "DISCHARGE CHECKLIST" in text_upper
    ):
        return {
            "type": "administrative_document"
        }

    # =========================
    # ER OBSERVATION CHART
    # =========================

    if (
        "ER OBSERVATION CHART" in text_upper
        or "VITAL PARAMETERS" in text_upper
    ):
        return {
            "type": "observation_chart"
        }

    # =========================
    # DISCHARGE SUMMARY
    # =========================

    if (
        "COURSE IN THE HOSPITAL" in text_upper
        or "CONDITION AT DISCHARGE" in text_upper
        or (
            "DISCHARGE SUMMARY" in text_upper
            and "CHECK LIST" not in text_upper
        )
        or "DIAGNOSIS" in text_upper
    ):
        return {
            "type": "discharge_summary"
        }

    # =========================
    # LAB REPORT
    # =========================

    if (
        "HEMOGLOBIN" in text_upper
        or "PLATELET" in text_upper
        or "WBC" in text_upper
        or "CBC" in text_upper
        or "BIOCHEMISTRY" in text_upper
        or "LABORATORY" in text_upper
    ):
        return {
            "type": "lab_report"
        }

    # =========================
    # MEDICATION CHART
    # =========================

    if (
        "TAB." in text_upper
        or "MEDICATION" in text_upper
        or "DOSAGE" in text_upper
        or "PRESCRIPTION" in text_upper
    ):
        return {
            "type": "medication_chart"
        }

    # =========================
    # NURSING NOTE
    # =========================

    if (
        "NURSING NOTE" in text_upper
        or "NURSES NOTE" in text_upper
    ):
        return {
            "type": "nursing_note"
        }

    return {
        "type": "unknown"
    }