```markdown
# Airline Analytics Platform

**End-to-End Airline Analytics Platform** with **Flight Delay Prediction, Cancellation Insights, Sales Forecasting, and Power BI Dashboards** built using Python, Streamlit, SQL, and Machine Learning.

---

## 🚀 Project Overview

This platform provides a **complete airline analytics solution** for tracking flights, predicting delays and cancellations, analyzing sales & revenue, and visualizing airline operations through **interactive dashboards**.

It integrates:
- **Real-time flight tracking**
- **Machine Learning models** for delay & cancellation prediction
- **ETL pipelines** for sales and flight data
- **Power BI dashboards** for operations, revenue, and comparisons

The platform is designed for **airline operations teams, analysts, and management** to make **data-driven decisions**.

---

## 📌 Features

- **Flight Tracker:** Track flights live with origin, destination, and flight status  
- **Delay Analyzer:** Analyze delay patterns using historical flight & weather data  
- **Delay Prediction:** ML model predicts flight delays based on multiple features  
- **Cancellation Prediction:** Predict likelihood of flight cancellations  
- **Sales Insights:** Analyze ticket sales, revenue trends, and class-wise distribution  
- **Revenue Forecasting:** Forecast airline revenue using historical sales data  
- **Airport & Weather Analysis:** Assess weather-related impacts on flight delays  
- **Airline Comparison:** Compare airlines across delay metrics and sales performance  
- **Power BI Dashboards:** Visual insights into revenue, operations, and KPIs  

---

## 📂 Project Structure

```

airline_analytics_platform/
├─ app.py                  # Streamlit main app
├─ app_pages/              # Modular Streamlit pages
├─ assets/                 # Images and icons
├─ dashboard/              # Power BI dashboards and PDFs
├─ data/                   # Sample flight & sales data
├─ models/                 # ML models and training scripts
├─ scripts/                # ETL, preprocessing, training scripts
├─ sql/                    # Database schema and ER diagrams
├─ utils/                  # Helper functions for DB, API, ML
├─ test_api.py             # API testing scripts
├─ test_sql_upload.py      # Database testing scripts
├─ requirements.txt        # Python dependencies
├─ README.md               # This file
└─ .gitignore              # Files to ignore

````

---

## 🛠️ Tech Stack

| Layer              | Technology/Tool |
|-------------------|----------------|
| Frontend           | Streamlit       |
| Backend            | Python (Flask optional) |
| ML Models          | Scikit-learn, XGBoost (custom models) |
| Data Processing    | Pandas, Numpy |
| Database           | MySQL / SQLite |
| Visualizations     | Matplotlib, Seaborn, Power BI |
| Deployment         | Local / Cloud (Streamlit / Render / Hugging Face) |

---

## 📝 How to Run Locally

1. **Clone the repo**  
```bash
git clone https://github.com/KajolVinodGupta/Airline-Analytics-Platform.git
cd Airline-Analytics-Platform
````

2. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Streamlit app**

```bash
streamlit run app.py
```

---

## 📊 Screenshots

*(Replace these placeholders with your actual screenshots)*

**Flight Tracker Page**
![Flight Tracker](assets/flight-tracker.png)

**Delay Analyzer Page**
![Delay Analyzer](assets/airplane.png)

**Revenue Dashboard**
![Power BI Revenue](dashboard/powerbi_revenue.png)
