PENDING_PATTERNS = [
    "report awaited",
    "results pending",
    "culture awaited",
    "follow up result",
    "pending"
]


def extract_pending(text):

    findings = []

    lower = text.lower()

    for pattern in PENDING_PATTERNS:

        if pattern in lower:

            sentences = text.split(".")

            for sentence in sentences:

                if pattern in sentence.lower():

                    findings.append(
                        sentence.strip()
                    )

    return list(
        set(findings)
    )