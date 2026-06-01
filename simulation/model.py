import simpy
from simulation.entities import Patient, Priority
from simulation.distributions import (
    inter_arrival_time, registration_time, triage_time,
    treatment_time, assign_priority, exit_type
)

class IGDSimulation:
    def __init__(self, params: dict, state_callback=None):
        self.params          = params
        self.state_callback  = state_callback
        self.env             = simpy.Environment()
        self.patients        = []
        self.patient_id      = 0
        self.registration    = simpy.Resource(
            self.env, capacity=params.get("n_registration", 1))
        self.triage          = simpy.Resource(
            self.env, capacity=params.get("n_nurses", 1))
        self.doctors         = simpy.PriorityResource(
            self.env, capacity=params.get("n_doctors", 3))
        self.stage_counts    = {
            "arrival": 0, "registration": 0, "triage": 0,
            "queue": 0, "treatment": 0, "exit": 0
        }
        self.utilization_log = []

    def _emit(self):
        if self.state_callback:
            self.state_callback({
                "time":         self.env.now,
                "stage_counts": dict(self.stage_counts),
                "patients":     [vars(p) for p in self.patients]
            })

    def patient_process(self, patient: Patient):
        # Event 1: Arrival
        self.stage_counts["arrival"] += 1
        self._emit()

        # Event 2-3: Registration
        self.stage_counts["arrival"] -= 1
        self.stage_counts["registration"] += 1
        with self.registration.request() as req:
            yield req
            yield self.env.timeout(registration_time())
            patient.registration_end = self.env.now
        self.stage_counts["registration"] -= 1

        # Event 4-5: Triage
        self.stage_counts["triage"] += 1
        with self.triage.request() as req:
            yield req
            yield self.env.timeout(triage_time())
            patient.triage_end = self.env.now
        self.stage_counts["triage"] -= 1

        # Event 6: Priority assignment
        patient.priority = assign_priority(
            self.params.get("triage_probs"))

        # Event 7: DOA check
        if patient.priority == 5:
            patient.exit_type = "DOA"
            self.stage_counts["exit"] += 1
            self._emit()
            return

        # Event 7-8: Queue entry
        self.stage_counts["queue"] += 1
        self._emit()

        # Event 9-10: Treatment
        with self.doctors.request(
                priority=patient.priority) as req:
            yield req
            patient.treatment_start = self.env.now
            self.stage_counts["queue"] -= 1
            self.stage_counts["treatment"] += 1
            self._emit()
            yield self.env.timeout(
                treatment_time(patient.priority))
            patient.treatment_end = self.env.now

        # Event 11-12: Exit
        patient.exit_type = exit_type(patient.priority)
        self.stage_counts["treatment"] -= 1
        self.stage_counts["exit"] += 1
        self._emit()

    def arrival_generator(self):
        while True:
            yield self.env.timeout(
                inter_arrival_time(self.params["lambda"]))
            self.patient_id += 1
            p = Patient(
                id=self.patient_id,
                priority=0,
                arrival_time=self.env.now)
            self.patients.append(p)
            self.env.process(self.patient_process(p))

    def run(self) -> dict:
        self.env.process(self.arrival_generator())
        self.env.run(until=self.params.get("duration", 480))
        return {
            "patients":     self.patients,
            "stage_counts": self.stage_counts,
            "time":         self.env.now
        }
