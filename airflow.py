from airflow import DAG
import pendulum
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
PROJE_AD = "angelic-gift-431019-i2"
DB_AD = "de_stock"

dag =  DAG(
    dag_id="18_GCSToBigQuery",
    schedule="@daily",
    start_date=pendulum.datetime(2023,5,31,tz="UTC"),
    catchup=False, # he catchup parameter in Apache Airflow determines whether a DAG will run missed past schedules
    )

sorgu =f"Select * from {PROJE_AD}.{DB_AD}.stock  where Price_Each > 1000"

create_new_table = BigQueryExecuteQueryOperator(
        task_id = "create_new_table",
        sql=sorgu,
        destination_dataset_table=f"{PROJE_AD}.{DB_AD}.analysis_project",
        create_disposition="CREATE_IF_NEEDED", 
        write_disposition="WRITE_TRUNCATE",#  WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default",
        dag=dag
    )
create_new_table