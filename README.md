# IGD Emergency Room Queue Simulation 🏥

A Discrete Event Simulation (DES) of a hospital Emergency Department (IGD) to optimize patient flow and resource allocation. This project uses stochastic modeling to transition from basic M/M/1 queuing up to complex M/M/c priority queuing systems.

## 🔬 Core Technologies
- **Simulation Engine:** `SimPy` (Python)
- **Data & Math:** `pandas`, `numpy`
- **Dashboard & Visualization:** `Streamlit`, `Plotly`, `matplotlib`

## 📊 The Mathematical Model
This simulation uses **Stochastic Priority Queues** modeled with Triangular distributions to closely mimic real-world emergency room variance. 

### Key Variables & Parameters:
- **`lambda` (Arrival Rate):** The average number of patients arriving per hour (modeled via exponential inter-arrival times).
- **`n_doctors` (c):** Number of doctors available for treatment.
- **`n_nurses` (s):** Number of nurses handling the triage phase.
- **`n_registration`:** Number of staff handling initial patient registration.
- **`duration`:** Total length of the simulation run in minutes.
- **`triage_probs`:** The probability distribution dividing incoming patients into 5 priority levels:
  - 🔴 **Red (Priority 1):** Critical / Resuscitation. Handled immediately.
  - 🟡 **Yellow (Priority 2):** Emergency.
  - 🟢 **Green (Priority 3):** Urgent.
  - ⚪ **White (Priority 4):** Non-urgent.
  - ⬛ **Black (Priority 5):** Dead on Arrival (DOA). Exits the system immediately without utilizing hospital beds.

### Process Flow Distributions:
- **Registration Time:** Triangular (1, 3, 5 minutes)
- **Triage Time:** Triangular (2, 5, 8 minutes)
- **Treatment Time:** Triangular distributions scaled dynamically by priority level:
  - Red: ~60 mins
  - Yellow: ~45 mins
  - Green: ~20 mins
  - White: ~15 mins

## 🚀 How to Run the Project

### 1. Install Dependencies
Ensure you have Python 3.9+ installed. Then install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Launch the Interactive Dashboard
The easiest way to interact with the model is via the Streamlit dashboard, which includes real-time animation, KPI metrics, and a Monte Carlo Sensitivity Analysis suite.
```bash
streamlit run dashboard/app.py
```

### 3. Run Headless Experiments (CLI)
To bypass the UI and directly run the raw Monte Carlo experiments and sensitivity analysis scripts in your terminal:
```bash
python run_experiments.py
```

## 🧪 Experiments Conducted
- **Experiment A (Doctor Count):** Sensitivity analysis varying the number of doctors to observe resource utilization and wait time reductions.
- **Experiment B (Arrival Rate):** Stress-testing the system by varying `lambda` to observe queue saturation and test priority preservation logic.
- **Experiment C (Monte Carlo):** N=100 replications to generate 95% Confidence Intervals and calculate the absolute risk probabilities (e.g., *Probability a Red patient waits > 5 minutes*), culminating in an optimal staffing recommendation algorithm.
