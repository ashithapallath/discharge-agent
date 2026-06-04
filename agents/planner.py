def planner(state):

    if state.failed_tools:
        return "recover"

    if not state.extracted_data:
        return "extract_information"

    if state.conflicts:
        return "resolve_conflicts"

    if state.pending_results:
        return "flag_pending"

    if state.medication_flags:
        return "review_medications"

    return "generate_summary"