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

sorgu =f"""
SELECT 
    *,
    CASE 
        WHEN previous_close = 0 THEN NULL  
        ELSE ABS(current_price - previous_close) / previous_close * 100 
    END AS change_percentage,
    AVG(current_price) OVER (PARTITION BY symbol, DATE(CURRENT_TIMESTAMP) ORDER BY CURRENT_TIMESTAMP ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS daily_average_price
FROM 
    de_stock.stock
WHERE 
    previous_close IS NOT NULL 
    AND current_price IS NOT NULL 
    AND previous_close != 0  -- previous_close sıfır olmayanları kontrol et
    AND ABS(current_price - previous_close) / previous_close > 0.10
ORDER BY 
    change_percentage desc;
"""
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