from tools.extractor import extract
from tools.pending_detector import extract_pending
from tools.conflict_checker import detect_conflicts
from tools.safety_validator import validate
from tools.page_classifier import classify_page
from tools.medication_reconciliation import (
    reconcile_medications
)


class DischargeAgent:

    def run(self, pages):

        print("\n=== RUNNING AGENT ===")

        all_extractions = []

        MAX_PAGES = 25

        pending_results = []

        # =========================
        # PAGE PROCESSING
        # =========================

        for idx, page in enumerate(pages):

            if idx >= MAX_PAGES:

                print(
                    "\nIteration cap reached."
                )

                break

            page_text = page.get("text", "")

            if len(page_text.strip()) < 100:
                continue

            page_type = classify_page(
                page_text
            )

            page_category = (
                page_type.get(
                    "type",
                    "unknown"
                )
            )

            print(
                f"Page {page['page']} -> "
                f"{page_category}"
            )

            # =========================
            # SKIP NON-CLINICAL PAGES
            # =========================

            if page_category in [
                "administrative_document",
                "observation_chart",
                "unknown"
            ]:
                continue

            # =========================
            # PENDING RESULT DETECTION
            # =========================

            page_pending = extract_pending(
                page_text
            )

            for item in page_pending:

                if (
                    item
                    not in pending_results
                ):
                    pending_results.append(
                        item
                    )

            # =========================
            # ONLY EXTRACT RELEVANT PAGES
            # =========================

            if page_category not in [
                "discharge_summary",
                "medication_chart"
            ]:
                continue

            print(
                f"\nExtracting Page "
                f"{page['page']} "
                f"({len(page_text)} chars)"
            )

            result = extract(
                page_text
            )

            all_extractions.append(
                {
                    "page": page["page"],
                    "result": result
                }
            )

        # =========================
        # MERGED STRUCTURE
        # =========================

        merged = {
            "patient_demographics": None,
            "admission_date": None,
            "discharge_date": None,
            "principal_diagnosis": None,
            "secondary_diagnoses": [],
            "hospital_course": None,
            "procedures": [],
            "discharge_medications": [],
            "medication_reconciliation": [],
            "allergies": [],
            "follow_up_instructions": None,
            "discharge_condition": None
        }

        # =========================
        # MERGE RESULTS
        # =========================

        for item in all_extractions:

            result = item["result"]

            if not isinstance(
                result,
                dict
            ):
                continue

            for field in merged:

                if field not in result:
                    continue

                value = result[field]

                # =========================
                # HOSPITAL COURSE MERGE
                # =========================

                if (
                    field
                    == "hospital_course"
                ):

                    if (
                        isinstance(
                            value,
                            dict
                        )
                        and value.get(
                            "value"
                        )
                        not in [
                            "",
                            "MISSING",
                            "PENDING"
                        ]
                    ):

                        existing = merged.get(
                            field
                        )

                        if (
                            existing
                            and isinstance(
                                existing,
                                dict
                            )
                        ):

                            merged[field][
                                "value"
                            ] += (
                                " "
                                + value.get(
                                    "value",
                                    ""
                                )
                            )

                            merged[field][
                                "evidence"
                            ] += (
                                " "
                                + value.get(
                                    "evidence",
                                    ""
                                )
                            )

                        else:

                            merged[field] = (
                                value
                            )

                    continue

                # =========================
                # LIST MERGE
                # =========================

                if isinstance(
                    merged[field],
                    list
                ):

                    if isinstance(
                        value,
                        list
                    ):
                        merged[field].extend(
                            value
                        )

                # =========================
                # STRUCTURED FIELD MERGE
                # =========================

                elif merged[field] is None:

                    if isinstance(
                        value,
                        dict
                    ):

                        extracted_value = (
                            value.get(
                                "value",
                                ""
                            )
                        )

                        if (
                            extracted_value
                            not in [
                                "",
                                "MISSING",
                                "PENDING"
                            ]
                        ):
                            merged[field] = (
                                value
                            )

                    else:

                        merged[field] = (
                            value
                        )

        # =========================
        # REMOVE DUPLICATES
        # =========================

        merged[
            "secondary_diagnoses"
        ] = list(
            {
                str(x): x
                for x in merged[
                    "secondary_diagnoses"
                ]
            }.values()
        )

        merged["procedures"] = list(
            {
                str(x): x
                for x in merged[
                    "procedures"
                ]
            }.values()
        )

        merged[
            "discharge_medications"
        ] = list(
            {
                str(x): x
                for x in merged[
                    "discharge_medications"
                ]
            }.values()
        )

        merged["allergies"] = list(
            {
                str(x): x
                for x in merged[
                    "allergies"
                ]
            }.values()
        )

        pending_results = list(
            dict.fromkeys(
                pending_results
            )
        )

        # =========================
        # MED RECONCILIATION
        # =========================

        med_reconciliation = (
            reconcile_medications(
                [],
                merged[
                    "discharge_medications"
                ]
            )
        )

        # =========================
        # CONFLICTS
        # =========================

        conflicts = detect_conflicts(
            all_extractions
        )

        # =========================
        # FINAL SUMMARY
        # =========================

        summary = {

            "patient_demographics":
                merged[
                    "patient_demographics"
                ]
                or "MISSING",

            "admission_date":
                merged[
                    "admission_date"
                ]
                or "MISSING",

            "discharge_date":
                merged[
                    "discharge_date"
                ]
                or "MISSING",

            "principal_diagnosis":
                merged[
                    "principal_diagnosis"
                ]
                or "MISSING",

            "secondary_diagnoses":
                merged[
                    "secondary_diagnoses"
                ],

            "hospital_course":
                merged[
                    "hospital_course"
                ]
                or "MISSING",

            "procedures":
                merged[
                    "procedures"
                ],

            "discharge_medications":
                merged[
                    "discharge_medications"
                ],

            "medication_reconciliation":
                med_reconciliation,

            "allergies":
                merged[
                    "allergies"
                ],

            "follow_up_instructions":
                merged[
                    "follow_up_instructions"
                ]
                or "MISSING",

            "pending_results":
                pending_results,

            "discharge_condition":
                merged[
                    "discharge_condition"
                ]
                or "MISSING",

            "conflicts":
                conflicts
        }

        summary[
            "clinician_review_flags"
        ] = validate(
            summary
        )

        print(
            "\n=== MERGED SUMMARY ==="
        )
        print(summary)
        print(
            "======================"
        )

        return summary