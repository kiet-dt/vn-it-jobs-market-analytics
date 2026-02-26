import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import *

from schemas.jobs_schema import create_schema

def create_spark_connection():
    spark_conn = None

    try:
        spark_conn = SparkSession.builder \
            .appName("Spark") \
            .config("spark.jars",
                    "/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.4.2.jar,"
                    "/opt/spark/jars/kafka-clients-3.4.0.jar,"
                    "/opt/spark/jars/postgresql-42.6.0.jar") \
            .getOrCreate()

        spark_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connected successfully!")

    except Exception as e:
        logging.error(f'Spark connect failed: {e}')

    return spark_conn

def read_kafka_topic(spark_conn, topic):
    spark_df = None

    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', topic) \
            .load()

        logging.info(f'Kafka topic: {topic}')

    except Exception as e:
        logging.error(f'Kafka topic read failed: {e}')

    return spark_df

def parse_df(spark_df,schema):
    select_expr = spark_df.selectExpr('CAST(value AS STRING)') \
                          .select(from_json(col('value'),schema).alias('data')) \
                          .select('data.*')

    return select_expr

def write_to_postgres(batch_df, table):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/jobdb") \
        .option("dbtable", table) \
        .option("user", "postgres") \
        .option("password", "123456") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

if __name__ == "__main__":
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        df_raw = read_kafka_topic(spark_conn, 'itviec')

        df = parse_df(df_raw,create_schema)

    jobs_df = df.select("title", "company", "salary", "url", "locations")

    companies_df = df.select("company").distinct()

    skill_list = ["Python", "Spark", "Kafka", "SQL", "Hadoop"]
    skill_array_col = array(*[lit(skill) for skill in skill_list])

    df = df.withColumn(
        "skills_extracted",
        filter(
            skill_array_col,
            lambda x: col("skills").contains(x)
        )
    )

    skills_df = df.select(explode("skills_extracted").alias("skill")).distinct()

    job_skills_df = df.select(
        "url",
        explode("skills_extracted").alias("skill")
    )

    locations_df = df.select(explode("locations").alias("location")).distinct()

    location_jobs_df = df.select("url", explode("locations").alias("location")).distinct()
