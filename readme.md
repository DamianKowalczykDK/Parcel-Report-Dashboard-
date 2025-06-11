# 📦 Parcel Locker Management System

A Python-based system for managing parcels, deliveries, users, and parcel lockers. The application supports data validation, transformation, reporting, and parcel size analysis. It also includes a simple web UI built using **Streamlit**.

---

📁 Project Structure
`````
locker_streamlit/ 
├── send_parcel.py
src/
├── model.py
├── validator.py
├── converter.py 
├── repository.py
├── service.py
├── file_service.py
tests/
├── test_file_service/
│ ├── conftest.py
│ └── test_file_service.py
├── test_locker_streamlit/
│ ├── conftest.py
│ └── test_send_parcel.py
├── test_repository/
├── data_repository/
│   ├── conftest.py
│   └── test_data_repository.py
├── parcel_summary_repository/
│   ├── conftest.py
│   └── test_parcel_summary_repository.py
├── test_service/
│   ├── conftest.py
│   └── test_service.py
├── conftest.py
├── test_converter.py
├── test_model.py
├── test_validator.py

Pipfile / Pipfile.lock # Project dependencies
`````
___

## 🚀 Getting Started

1. Install Pipenv (if not already installed)\
   - pip install pipenv
2. Install dependencies
   - pipenv install
3. Activate the virtual environment
   - pipenv shell

## 🖥️ Running the Streamlit App (Web UI)
After activating the environment, run the Streamlit app:

streamlit run main_2.py
The app will open in your browser (usually at: http://localhost:8501).
Use the interface to view reports, parcel statistics, and visual summaries generated from the data.

## 🧠 Features
✅ Data validation (emails, positive numbers, required fields)

✅ Converters to transform raw dictionaries to structured data classes

✅ Repositories for managing users, lockers, parcels, and deliveries

✅ Reporting services:

Most common parcel sizes per locker

Cities with the most sent/received parcels by size

Longest delivery durations between send and expected date

Locker compartment limit checking

✅ Streamlit web UI for interacting with and viewing reports

## 🧪 Testing
pipenv install --dev\
Run unit tests:

pipenv run test
To check test coverage:

- pipenv run check     # runs pyright
- pipenv run check2    # runs mypy on src, locker_streamlit, tests, main.py, main1.py
- pipenv run test      # runs pytest with coverage reports


🛠 Technologies Used
Python 3.13.2

- Pipenv
- Streamlit
- email-validator
- dataclasses
- MyPy
- Pytest

## 🐳  Docker & Docker Compose
✅ Build and run the project using Docker Compose (recommended):
- docker-compose up -d --build

✅ You can also build the Docker image manually:
- docker build -t locker-monitor .

## 📄 Example Usage (Reports)

from src.repository import ParcelSummaryRepository
from src.service import ParcelReportService

repo = ParcelSummaryRepository(...)  # Initialized repositories
service = ParcelReportService(repository=repo)

print(service.most_common_parcel_sizes_per_locker())
print(service.city_most_shipments_by_size())
print(service.max_days_between_sent_and_expected())

## 📬 Author
Educational project — Parcel Locker Management System

Author: Damian Kowalczyk
\
Year: 2025

