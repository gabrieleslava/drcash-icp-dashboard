# 🎯 Dr.Cash — ICP & Clinic Retention Dashboard

A state-of-the-art, premium-looking analytical dashboard built in Python to discover the **Ideal Customer Profile (ICP)** and monitor **Clinic Cohort Retention** for **Dr.Cash**.

The application is styled with a gorgeous, high-end dark glassmorphism theme that features modern typography, sleek custom metric cards, dynamic filters, and advanced data visualization layouts.

---

## ✨ Features

- **📊 Tab 1: Visão Geral & ICP**:
  - **Custom KPI Cards**: Clean, modern cards tracking total acquired clinics, accumulated revenue, network penetration rate, and dominant specialty.
  - **Dynamic Filters**: Slice and dice demographic insights by State (UF), Specialty (Segmento), and registration Safra.
  - **Interactive Analytics**: Premium line graphs tracking faturamento growth over time, transaction values (Ticket Médio), and donut/bar charts breaking down network composition and specialties.
- **🎯 Tab 2: Matriz de Cohort & Retenção**:
  - **Relative Cohort Heatmap**: A classic SaaS retention grid aligning all cohorts at "Month 0" to compare clinic engagement rates over time.
  - **Dynamic Metric Comparer**: Compare any metrics (such as simulations, proposals initiated, approvals, and revenues) side-by-side across all registration cohorts with beautiful automated color highlighting.

---

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Data Engineering**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Data Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/) & [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
- **Styling**: Vanilla CSS, Outfit Font (Google Fonts)

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Clone and Navigate
```bash
cd drcash-icp-dashboard
```

### 3. Create a Virtual Environment (Optional but recommended)
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
This will spin up a development server and automatically open the application at `http://localhost:8501`.

---

## 📁 Repository Structure

```
drcash-icp-dashboard/
│
├── .streamlit/
│   └── config.toml          # Premium theme styling (Teal and Dark Slate)
│
├── cohort_drcash.csv        # Pre-aggregated cohort metrics
├── cohort_clinicas_drcash.csv # Detailed clinic demographic registry
│
├── app.py                   # Main Streamlit dashboard script
├── requirements.txt         # Package dependencies
├── .gitignore               # Standard Python & OS gitignore
└── README.md                # Premium project documentation
```

---

*Desenvolvido com 💚 para a equipe Dr.Cash.*
