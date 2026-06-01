from dataclasses import dataclass
from enum import IntEnum

class Priority(IntEnum):
    RED    = 1
    YELLOW = 2
    GREEN  = 3
    WHITE  = 4
    BLACK  = 5

@dataclass
class Patient:
    id:               int
    priority:         Priority
    arrival_time:     float
    registration_end: float = 0.0
    triage_end:       float = 0.0
    treatment_start:  float = 0.0
    treatment_end:    float = 0.0
    exit_type:        str   = ""

    @property
    def wait_time(self) -> float:
        """
        Time from triage end to treatment start.
        Returns 0.0 if treatment never began
        (patient still queuing at sim end).
        """
        if self.treatment_start == 0:
            return 0.0
        if self.triage_end == 0:
            return 0.0
        return self.treatment_start - self.triage_end

    @property
    def treatment_duration(self) -> float:
        """
        Actual completed treatment time only.
        Returns 0.0 for in-progress or untreated.
        Prevents negative utilization calculation.
        """
        if self.treatment_start == 0:
            return 0.0
        if self.treatment_end == 0:
            return 0.0
        return self.treatment_end - self.treatment_start

    @property
    def total_time(self) -> float:
        """
        Full IGD journey time.
        Returns 0.0 if not fully completed.
        """
        if self.treatment_end == 0:
            return 0.0
        return self.treatment_end - self.arrival_time

    @property
    def is_completed(self) -> bool:
        """True only if patient fully exited system."""
        return self.treatment_end > 0 or \
               self.exit_type == "DOA"
