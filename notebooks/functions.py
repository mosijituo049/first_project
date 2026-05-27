# Add all the imports needed by the functions in the project here
#================================================================
#
#================================================================

import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq
import yaml

with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

def clean_col_name(df_origin):
    df=df_origin.copy()

    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
    )
    
    return df

def data_loader():
    # read csv
    df_apps = pd.read_csv(config['input_data']['file_apps'])
    df_reviews = pd.read_csv(config['input_data']['file_reviews'])

    df_apps = clean_col_name(df_apps)
    df_reviews = clean_col_name(df_reviews)

    # DataFrame to BigQuery table
    tables = {
        "raw_apps": df_apps,
        "raw_reviews": df_reviews
    }

    # upload
    for table_name, dataframe in tables.items():

        print(f"Uploading {table_name}...")

        to_gbq(
            dataframe=dataframe,
            destination_table=f"{config['gcp']['dataset']}.{table_name}",
            project_id="ironhack-497023",
            if_exists="replace"
        )

    print("All tables uploaded successfully!")

def export_clean_data():
    client = bigquery.Client()

    # apps
    query_apps = f"""
    SELECT *
    FROM `{config['tables']['stg_apps']}`
    """
    
    df_apps = client.query(query_apps).to_dataframe()
    
    df_apps.to_csv(
        "../data/clean/clean_apps.csv",
        index=False
    )
    
    # reviews
    query_reviews = f"""
    SELECT *
    FROM `{config['tables']['stg_reviews']}`
    """
    
    df_reviews = client.query(query_reviews).to_dataframe()
    
    df_reviews.to_csv(
        "../data/clean/clean_reviews.csv",
        index=False
    )
    
    print("Clean data exported.")
