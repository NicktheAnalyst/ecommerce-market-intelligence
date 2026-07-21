# 🛒 E-Commerce Market Intelligence Platform

A production-grade Python market intelligence and analytics pipeline. The platform monitors competitor e-commerce platforms, ingests market and pricing data, processes real-time ETL runs in PostgreSQL, and delivers actionable pricing and stockout risk insights via an interactive Streamlit dashboard.

---

## 🌟 Key Features

- **Automated Web Scraping:** High-resilience web extraction engineered with **Playwright**.
- **Data Enrichment:** Real-time API integrations enriching competitor pricing and catalog metrics.
- **Robust Database Layer:** Relational data modeling using **PostgreSQL** & **SQLAlchemy ORM**.
- **Automated ETL Pipeline:** Modular data loader executing transformations, currency normalization, and risk flag computations.
- **Interactive Analytics Dashboard:** Real-time monitoring UI built with **Streamlit** (and Power BI support).
- **Automated Test Suite:** Comprehensive unit & integration testing built with **`pytest`**.

---

## 🏗️ Architecture & Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Database & ORM** | PostgreSQL, SQLAlchemy |
| **Web Scraping** | Playwright |
| **Data Processing** | Pandas |
| **Visualization** | Streamlit, Power BI |
| **Testing** | Pytest |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have **Python 3.11+** and **PostgreSQL** installed and running locally.

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-market-intelligence.git
cd ecommerce-market-intelligence

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
