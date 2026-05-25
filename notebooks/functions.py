# Add all the imports needed by the functions in the project here
#================================================================
#
#================================================================

import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq

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
    df_apps = pd.read_csv("../data/raw/raw_googleplaystore.csv")
    df_reviews = pd.read_csv("../data/raw/raw_googleplaystore_user_reviews.csv")

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
            destination_table=f"google_play_store_apps.{table_name}",
            project_id="ironhack-497023",
            if_exists="replace"
        )

    print("All tables uploaded successfully!")
