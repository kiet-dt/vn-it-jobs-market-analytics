import logging
from pyspark.sql import SparkSession
# from pyspark.sql import functions as F
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

def parse_df(df_raw,schema):
    return df_raw.selectExpr('CAST(value AS STRING)') \
                          .select(from_json(col('value'),schema).alias('data')) \
                          .select('data.*')

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

    if spark_conn is None:
        exit(1)

    df_raw = read_kafka_topic(spark_conn, 'itviec')

    df = parse_df(df_raw,create_schema)

    skill_list = [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "PHP", "Ruby", "Swift", "Kotlin", "Dart", "Scala", "MATLAB",
        "HTML", "CSS", "Sass", "Less", "Tailwind CSS", "Bootstrap", "React.js","ReactJS", "Vue", "VueJS","Vue.js", "Angular", "Next.js","NextJS", "Nuxt.js", "Redux", "Webpack", "Vite","RESTful API", "API RESTful",
        "Node.js", "Express", "NestJS", "Django", "Flask", "FastAPI", "Spring", "Spring Boot", ".NET", "ASP.NET", "Laravel", "Ruby on Rails",
        "SQL", "MySQL", "PostgreSQL", "Oracle", "SQL Server", "MongoDB", "Redis", "Cassandra", "DynamoDB", "Elasticsearch","Rabbit MQ",
        "Docker", "Kubernetes", "K8s", "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "Terraform", "Ansible", "Nginx", "Apache", "AWS", "Azure", "GCP",
        "Hadoop", "Spark", "PySpark", "Kafka", "Flink", "Airflow", "Hive", "HBase", "Snowflake", "Databricks", "dbt","Playwright",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost", "NLP", "LLM", "OpenCV",
        "Android", "iOS", "Flutter", "React Native", "Xamarin",
        "Selenium", "JUnit", "TestNG", "Cypress", "Postman",
        "OWASP","Cryptography","SIEM", "SOC",
        "Linux","TCP/IP", "DNS","Firewall","VMware","Bash","Shell Script",
        "Git", "GitHub", "GitLab","Bitbucket","Jira", "Confluence",
        "Excel","BI","Tableau","Google Data Studio","Looker","BigQuery","Redshift","Grafana",
        "Unity"
        ]
    skill_array_col = array(*[lit(skill) for skill in skill_list])

    df = df.withColumn(
        "skills_extracted",
        filter(
            skill_array_col,
            lambda x: col("skills").contains(x)
        )
    )


    def process_batch(batch_df, batch_id):

        print(f"Processing batch {batch_id}")

        jobs_df = batch_df.select("title", "company", "salary", "url", "locations")
        write_to_postgres(jobs_df, "jobs")

        companies_df = batch_df.select("company").distinct()
        write_to_postgres(companies_df, "companies")

        skills_df = batch_df.select(explode_outer("skills_extracted").alias("skill")).filter(col("skill").isNotNull())
        write_to_postgres(skills_df, "skills")

        job_skills_df = batch_df.select(
            "url",
            explode_outer("skills_extracted").alias("skill")).filter(col("skill").isNotNull())
        write_to_postgres(job_skills_df, "job_skills")

        locations_df = batch_df.select(explode_outer("locations").alias("location")).filter(col("location").isNotNull())
        write_to_postgres(locations_df, "locations")

        location_jobs_df = batch_df.select("url", explode_outer("locations").alias("location")).filter(col("location").isNotNull())
        write_to_postgres(location_jobs_df, "location_jobs")


    query = df.writeStream \
        .foreachBatch(process_batch) \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/checkpoints/itviec") \
        .start()

    query.awaitTermination()