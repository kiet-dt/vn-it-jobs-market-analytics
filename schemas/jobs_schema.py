from pyspark.sql.types import *

def create_schema():
    schema = StructType([
        StructField('title', StringType(), True),
        StructField('company', StringType(), True),
        StructField('salary', StringType(), True),
        StructField('url', StringType(), True),
        StructField('locations', ArrayType(StringType()), True),
        StructField('skills', StringType(), True)
    ])

    return schema