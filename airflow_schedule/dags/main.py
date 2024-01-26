from airflow import DAG
from datetime import datetime, timedelta, timezone
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
utc_plus_7 = timezone(timedelta(hours=7))

import requests




default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 11, tzinfo=utc_plus_7),
    'retries': 1,
    'retry_delay': timedelta(hours=1),
}

def get_url():
    res = requests.get('http://host.docker.internal:3000/updatedata')
    print(res)


with DAG(
    dag_id = 'crawler_data',
    default_args=default_args,
    description='dag handle crawler data',
    start_date=datetime(2024, 1, 16, tzinfo=utc_plus_7),
    schedule_interval='30 9 * * *',
) as dag:
    
    crawler_data = PythonOperator(
        task_id='cralwer',
        python_callable=get_url,
    )
    
    crawler_data
    