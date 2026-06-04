REQUIRED_FIELDS = [
    "principal_diagnosis",
    "hospital_course",
    "discharge_condition"
]

def validate(summary):

    flags = []

    for field in REQUIRED_FIELDS:

        value = summary.get(field)

        if (
            not value
            or value == "MISSING"
        ):

            flags.append(
                f"{field}: CLINICIAN REVIEW REQUIRED"
            )

    return flags