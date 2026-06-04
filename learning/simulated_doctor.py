class SimulatedDoctor:

    def review(self, summary):

        corrected = summary.copy()

        corrections = []

        if not corrected.get("pending_results"):

            corrected["pending_results"] = [
                "Check microbiology culture results"
            ]

            corrections.append(
                "missing_pending_results"
            )

        if not corrected.get(
            "follow_up_instructions"
        ):

            corrected[
                "follow_up_instructions"
            ] = "Follow up with primary care physician"

            corrections.append(
                "missing_followup"
            )

        return corrected, corrections