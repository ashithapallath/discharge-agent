from dataclasses import dataclass, field

@dataclass
class AgentState:

    raw_documents: list = field(default_factory=list)

    extracted_data: dict = field(default_factory=dict)

    conflicts: list = field(default_factory=list)

    pending_results: list = field(default_factory=list)

    medication_flags: list = field(default_factory=list)

    clinician_flags: list = field(default_factory=list)

    failed_tools: list = field(default_factory=list)

    trace: list = field(default_factory=list)

    completed: bool = False

    step_count: int = 0