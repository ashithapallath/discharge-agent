from difflib import SequenceMatcher


def calculate_reward(
    draft_summary,
    corrected_summary
):

    score = SequenceMatcher(
        None,
        str(draft_summary),
        str(corrected_summary)
    ).ratio()

    return round(score, 4)