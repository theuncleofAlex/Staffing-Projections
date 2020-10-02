from google.oauth2 import service_account
from google.cloud import bigquery

key_path = "Staffing Projections-425ff1698984.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials)


def replace_null(filename, new_filename):
    null_str = 'NULL'
    with open(filename, "rt") as fin:
        with open(new_filename, "wt") as fout:
            for line in fin: fout.write(line.replace(null_str, ''))
    fin.close()
    fout.close()


def load_table(table_id, filename, schema):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=0, schema=schema
    )

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


dataset_id = "staffing-projections.raw_data"
replace_null("RawData/outbounddialercalls.csv", "RawData/processed-outbound-monthly.csv")
# load_table(
#     table_id="%s.programs" % dataset_id,
#     filename="RawData/programs.csv",
#     schema=[
#         bigquery.SchemaField("program_id", "INT64"),
#         bigquery.SchemaField("p_name", "STRING"),
#         bigquery.SchemaField("p_abbrev", "STRING"),
#     ]
# )

# load_table(
#     table_id="%s.inbound_monthly" % dataset_id,
#     filename="RawData/processed-inbound-monthly.csv",
#     schema=[
#         bigquery.SchemaField("mid", "INT64"),
#         bigquery.SchemaField("program_id", "INT64"),
#         bigquery.SchemaField("time_offered", "TIMESTAMP"),
#         bigquery.SchemaField("time_answered", "TIMESTAMP"),
#         bigquery.SchemaField("time_terminated", "TIMESTAMP"),
#     ]
# )

load_table(
    table_id="%s.outbound_monthly" % dataset_id,
    filename="RawData/processed-outbound-monthly.csv",
    schema=[
        bigquery.SchemaField("when_called", "TIMESTAMP"),
        bigquery.SchemaField("inbound_id", "INT64"),
        bigquery.SchemaField("consult_id", "INT64"),
        bigquery.SchemaField("program_id", "INT64"),
    ]
)