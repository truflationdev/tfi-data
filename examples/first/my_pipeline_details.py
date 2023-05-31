from truflation.data.pipeline_details import PipeLineDetails
from truflation.data.source_details import SourceDetails
from truflation.data.export_details import ExportDetails
from dotenv import load_dotenv
import os

load_dotenv()
DB_PASS = os.getenv('DB_PASS')

# Name
pipeline_name = "Hello World"


def pre_ingestion_function():
    print(f'I do this before ingestion')


def post_ingestion_function():
    print(f'I do this after ingestion')


# Source Types: csv, API, Excel, Google Sheet, TrueData
sources = [
    # name, source_type, source, parser function (default is pass through))
    SourceDetails("first", "csv", "examples/first/example.csv"),
    SourceDetails("second", "csv", "examples/first/example_2.csv", lambda x: x)
]

exports = [
    ExportDetails(
        name='sum',
        connector = f'mariadb+pymysql://root:{DB_PASS}@api-test.truflation.io:3306/timeseries',
        key='work_details'
    )
]

def transformer(data_dict: dict):
    df1 = data_dict['first']
    df2 = data_dict['second']
    res_df = df1.copy()
    res_df["value"] = df1["value"].add(df2["value"])

    res_dict = {"sum": res_df}
    return res_dict


def get_details():
    my_pipeline = PipeLineDetails(name=pipeline_name,
                                  sources=sources,
                                  exports=exports,
                                  pre_ingestion_function=pre_ingestion_function,
                                  post_ingestion_function=post_ingestion_function,
                                  transformer=transformer
                                  )
    return my_pipeline


if __name__ == "__main__":
    get_details()
