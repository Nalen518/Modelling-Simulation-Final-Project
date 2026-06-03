<h1 align="center">🏥 IGD Queue Optimization</h1>
<p align="center">
  <b>Emergency Room Discrete Event Simulation — Triage-Based Patient Flow Analysis</b>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SimPy-DES_Engine-2E86C1" alt="SimPy">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Monte_Carlo-N%3D100-ffc176" alt="Monte Carlo">
</p>

---

## 📖 About

A **Discrete Event Simulation (DES)** of a hospital Emergency Department (IGD/Instalasi Gawat Darurat) built for the **Modeling & Simulation Final Project**. The application models patient flow through registration, triage, priority queueing, and doctor treatment using stochastic processes — then uses **Monte Carlo methods** (N=100 replications) to derive risk probabilities and staffing recommendations.

### Key Features

| Feature | Description |
|---------|-------------|
| 🎬 **Live Animation** | Real-time patient flow visualization with KPI sparklines and event log |
| 📊 **Simulation Dashboard** | Priority breakdown tables, waiting time distributions, discharge/admission charts, and doctor utilization gauge |
| 🔬 **Sensitivity Analysis** | Predefined scenario comparison (2/3/4 doctors) with automated insight generation |
| 🎲 **Monte Carlo Analysis** | 4 research questions: optimal staffing, overload probability, critical patient risk, and operational risk indicators |
| 📚 **Methodology & Theory** | Built-in documentation of model scope, assumptions, parameter justifications, and queueing theory foundations |

---

## 🚀 Quick Start

### 1. Download & Extract

```bash
# Clone the repository
git clone https://github.com/Nalen518/Modelling-Simulation-Final-Project.git
cd Modelling-Simulation-Final-Project
```

Or click **Code → Download ZIP** on GitHub and extract the folder.

### 2. Install Dependencies

Make sure you have **Python 3.9+** installed, then:

```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
igd-simulation/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── dashboard/
│   ├── app.py                # Main Streamlit application (all tabs)
│   ├── animation_component.py # Live patient flow animation (HTML/JS)
│   └── styles.py             # CSS design system & UI components
├── simulation/
│   ├── model.py              # SimPy DES engine (IGDSimulation class)
│   ├── entities.py           # Patient dataclass & computed properties
│   ├── distributions.py      # Stochastic distributions (Poisson, Triangular)
│   └── analysis.py           # Metrics, experiments, Monte Carlo functions
├── data/
│   └── results/              # Output directory for experiment results
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🔬 The Mathematical Model

### Queueing Model Progression

| Model | Description |
|-------|-------------|
| **M/M/1** | Single-server baseline (1 doctor) |
| **M/M/S** | Multi-server with S nurses at triage |
| **M/M/C** | Multi-server with C doctors + priority queueing |

### Stochastic Distributions

| Process | Distribution | Parameters |
|---------|-------------|------------|
| Patient Arrivals | Poisson (exponential inter-arrival) | λ = 1–50 pts/hr |
| Registration | Triangular | (1, 2, 5) minutes |
| Triage | Triangular | (1, 3, 8) minutes |
| Treatment (Red) | Triangular | (45, 90, 180) minutes |
| Treatment (Yellow) | Triangular | (20, 40, 90) minutes |
| Treatment (Green) | Triangular | (10, 20, 45) minutes |
| Treatment (White) | Triangular | (5, 8, 20) minutes |

### 5-Level Triage Classification

| Level | Name | Default % | Description |
|-------|------|-----------|-------------|
| 🔴 P1 | Red | 5% | Critical / Resuscitation |
| 🟡 P2 | Yellow | 20% | Emergency |
| 🟢 P3 | Green | 55% | Urgent |
| ⚪ P4 | White | 19% | Non-urgent |
| ⬛ P5 | Black | 1% | Dead on Arrival (DOA) |

---

## 📊 Dashboard Tabs

### Tab 1: Animation
Real-time patient flow visualization showing patients moving through Arrival → Registration → Triage → Priority Queue → Doctor Treatment → Discharge/Admission. Includes live KPI cards, queue summary, waiting time histogram, and event log.

### Tab 2: Simulation
Detailed results from the current run: KPI metrics (2×3 grid), per-priority breakdown table, waiting time distribution histogram, priority donut chart, discharge vs admission bar chart, doctor utilization gauge, and Kemenkes clinical validation.

### Tab 3: Sensitivity Analysis
- **Predefined Scenario Analysis**: Compare 2, 3, and 4 doctors with automated insights and staffing recommendations.
- **Experiment A**: Vary doctor count (c = 2, 3, 4, 5) at fixed λ = 20.
- **Experiment B**: Vary arrival rate (λ = 10, 20, 30, 40) at fixed c = 3.

### Tab 4: Monte Carlo
Four research questions answered using N=100 replications per scenario:
- **Q1**: How many doctors are needed? (scans c=1..10)
- **Q2**: What is P(system overloaded)? (varies λ=10,20,30,40)
- **Q3**: Will critical patients wait too long? (95% CI analysis)
- **Q4**: Operational Risk Indicators (P(Queue>50), P(Wait>30min), P(Util>90%), P(Red Wait>5min))

### Tab 5: Methodology & Theory
Built-in academic documentation covering model scope (inside vs outside), core assumptions, limitations, parameter sources, Poisson arrival theory with LaTeX notation, and DES vs Monte Carlo methodology comparison.

---

## ⚙️ Configurable Parameters

All parameters are adjustable via the sidebar:

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Arrival Rate (λ) | 1–50 pts/hr | 20 | Poisson arrival intensity |
| Doctors (c) | 1–10 | 3 | Treatment server capacity |
| Triage Nurses (s) | 1–5 | 1 | Triage assessment capacity |
| Registration Staff | 1–3 | 1 | Registration counter capacity |
| Duration | 60–1440 min | 480 | Simulation run length (8-hr shift) |
| Triage Probabilities | 0–100% each | See above | Must sum to 100% |

---

## 👥 Authors

Modeling & Simulation Final Project Team

---

## 📄 License

This project is for **educational and research purposes only**. The simulation results should not be used for clinical decision-making or real-world hospital staffing.
