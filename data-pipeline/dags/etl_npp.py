from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

from utils import run_query

def extract_data():
    file_path = '/opt/airflow/data/STATISTIK LPBBTI Desember 2024 (1) _ For Testing .xlsx'
    sheet_name = '18'  

    dates_raw = pd.read_excel(file_path, sheet_name=sheet_name, usecols="C:O", skiprows=1, nrows=1, header=None)
    npp_raw = pd.read_excel(file_path, sheet_name=sheet_name, usecols="C:O", skiprows=43, nrows=1, header=None)

    return dates_raw, npp_raw

def transform_data(ti):
    # Pull the extracted data from the extract task
    dates_raw, npp_raw = ti.xcom_pull(task_ids='extract_data')

    # Validate the data to make sure it follows the condition (i.e., data is increasing)
    for i in range(1, len(npp_raw.columns)):
        if npp_raw.iloc[0, i] < npp_raw.iloc[0, i - 1]:
            raise ValueError(f"Validation failed: npp_raw[{i}] < npp_raw[{i - 1}]")

    # Transform dates to 'MMM-YYYY' format (as a list of strings)
    dates_transformed = pd.to_datetime(dates_raw.iloc[0]).dt.strftime('%b-%Y').tolist()

    # Convert DataFrame row to a list (this converts the row of numbers to a list of integers)
    npp_data = npp_raw.iloc[0].tolist()

    # Return both dates_transformed and data_transformed as simple lists (JSON-serializable)
    return dates_transformed, npp_data

def load_data(ti):
    dates_transformed, npp_data = ti.xcom_pull(task_ids='transform_data')

    inserted_data = []
    for month, value in zip(dates_transformed, npp_data):
        inserted_data.append((month, value))

    insert_query = "INSERT INTO DWH.NPP (bulan, npp) VALUES %s"
    run_query(insert_query,'afpi-recruitment-test-conn', inserted_data)
    print("NPP data inserted into database successfully.")

with DAG("etl_npp",
        start_date=datetime(2025, 1, 1),
        schedule_interval="@monthly",
        catchup=False) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task