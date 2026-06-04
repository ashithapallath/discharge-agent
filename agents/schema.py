from pydantic import BaseModel
from typing import List


class DischargeSummary(BaseModel):

    patient_demographics: str

    admission_date: str

    discharge_date: str

    principal_diagnosis: str

    secondary_diagnoses: List[str]

    hospital_course: str

    procedures: List[str]

    allergies: str

    discharge_medications: List[str]

    medication_changes: List[str]

    follow_up_instructions: str

    pending_results: List[str]

    discharge_condition: str

    conflicts: List[str]

    clinician_review_flags: List[str]