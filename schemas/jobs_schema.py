from pyspark.sql.types import *

def create_jobs_schema():
    jobs_schema = StructType([
        StructField('title', StringType(), True),
        StructField('company', StringType(), True),
        StructField('salary', StringType(), True),
        StructField('url', StringType(), True),
        StructField('locations', ArrayType(), True),
        StructField('skills', ArrayType(), True)
    ])

    return jobs_schema