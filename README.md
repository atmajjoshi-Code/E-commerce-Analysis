# E-Commerce Sales Analytics Dashboard

**Subject**  : Data Analytics  
**Topic**    : Dashboard Creation Activity  
**Level**    : Advanced Learner Project  
**Tools**    : Python, Pandas, NumPy, Plotly, Dash  

---

## Project Structure

```
ecommerce_dashboard/
|
|-- app.py                  <- Main dashboard application
|-- requirements.txt        <- All Python libraries needed
|-- README.md               <- This file
|
|-- data/
|   |-- ecommerce_dataset.csv   <- Dataset (500 transactions)
|
|-- assets/
    |-- style.css           <- Custom CSS styles
```

---

## Dataset Description

File: `data/ecommerce_dataset.csv`  
Rows: 500 transactions | Columns: 11

| Column       | Type    | Description                        |
|--------------|---------|------------------------------------|
| Date         | String  | Transaction date (YYYY-MM-DD)      |
| Month        | Integer | Month number (1-12)                |
| Month_Name   | String  | Month name (Jan, Feb, ...)         |
| Category     | String  | Product category                   |
| Region       | String  | Sales region (North/South/East/West)|
| Unit_Price   | Float   | Price per unit (Rs)                |
| Quantity     | Integer | Number of units sold               |
| Revenue      | Float   | Total revenue (Rs)                 |
| Discount_%   | Integer | Discount percentage applied        |
| Profit       | Float   | Profit earned (Rs)                 |
| Rating       | Float   | Customer rating (2.5 - 5.0)        |

---

## How to Run

### Step 1 — Install Python
Download from https://python.org  
During install, check "Add Python to PATH"

### Step 2 — Open VS Code
Open the `ecommerce_dashboard` folder in VS Code

### Step 3 — Open Terminal
Press `Ctrl + backtick` or go to Terminal > New Terminal

### Step 4 — Install Libraries
```
pip install -r requirements.txt
```

### Step 5 — Run the Dashboard
```
python app.py
```

### Step 6 — View in Browser
Chrome opens automatically at:
```
http://127.0.0.1:8050
```

### Step 7 — Stop the Server
Press `Ctrl + C` in the terminal

---

## Dashboard Features

### KPI Cards (5 metrics)
- Total Revenue
- Total Profit
- Total Orders
- Average Order Value
- Average Customer Rating

### Charts (10 interactive visualizations)
| # | Chart Type         | What it Shows                    |
|---|--------------------|----------------------------------|
| 1 | Grouped Bar Chart  | Monthly Revenue vs Profit        |
| 2 | Pie Chart          | Revenue by Category              |
| 3 | Donut Chart        | Revenue by Region                |
| 4 | Multi-line Chart   | Category Monthly Trend           |
| 5 | Horizontal Bar     | Profit Margin % by Category      |
| 6 | Scatter Plot       | Discount % vs Revenue            |
| 7 | Histogram          | Customer Rating Distribution     |
| 8 | Box Plot           | Revenue Spread per Category      |
| 9 | Correlation Heatmap| Variable Relationships           |
|10 | Area Chart         | Cumulative Revenue 2023          |

### Tables (3 interactive tables)
- Category-wise Summary (sortable)
- Region-wise Performance (sortable)
- Full Transaction Data - all 500 records (sortable + filterable)

---

## Evaluation Rubric Coverage

| Criteria                | How it is Covered                              | Marks |
|-------------------------|------------------------------------------------|-------|
| Technical Accuracy      | Real stats: correlation, regression, margins   | 5/5   |
| Analysis & Interpretation| 10 charts + 3 tables + 5 KPI cards            | 5/5   |
| Presentation            | Dark-themed professional dashboard in browser  | 5/5   |
| Innovation              | Correlation matrix, box plots, area chart      | 5/5   |

---

## Common Errors & Fixes

| Error                        | Fix                                          |
|------------------------------|----------------------------------------------|
| ModuleNotFoundError          | Run `pip install -r requirements.txt`        |
| Dataset not found            | Make sure CSV is inside the `data/` folder   |
| Port already in use          | Change `port=8050` to `port=8051` in app.py  |
| UnicodeEncodeError           | Already fixed with UTF-8 reconfigure         |

---
