# VN IT Jobs Market Analytics

A data pipeline for collecting, streaming, and analyzing IT job listings from the Vietnamese job market. The project crawls job data from [ITViec](https://itviec.com), streams it through Apache Kafka, and processes it with PySpark before loading into PostgreSQL for analytics.

## Overview

- **Crawler**: Scrapy spider that scrapes IT job postings (title, company, salary, locations, skills, URL) from itviec.com.
- **Streaming**: Job items are published to a Kafka topic and consumed by a Spark Structured Streaming job.
- **Processing**: Spark parses JSON, normalizes skills against a predefined list, and writes to PostgreSQL staging tables (jobs, companies, skills, job_skills, locations, job_locations).
- **Infrastructure**: Docker Compose runs Zookeeper, Kafka (Confluent), Schema Registry, Confluent Control Center, and a Spark cluster (master + worker).

## Architecture

![Architecture](images/architecture.png)

## Database Schema

![Database ERD](images/erd.png)

## Prerequisites

- **Docker** and **Docker Compose**
- **Python 3** (for running the Scrapy crawler locally)
- **PostgreSQL** (for Spark to write staging data; default config points to `host.docker.internal:5432/jobdb`)

## Project Structure

```
vn-it-jobs-market-analytics/
├── crawler/                    # Scrapy project
│   └── crawler/
│       ├── items.py            # JobItem definition
│       ├── pipelines.py        # Kafka producer pipeline
│       ├── settings.py
│       └── spiders/
│           └── itviec_spider.py # ITViec spider
├── schemas/
│   └── jobs_schema.py          # PySpark schema for job JSON
├── spark_stream.py             # Spark Structured Streaming job (Kafka → PostgreSQL)
├── docker-compose.yaml        # Kafka, Zookeeper, Schema Registry, Control Center, Spark
├── Dockerfile                 # Spark image with Python deps
└── requirements.txt           # kafka-python, scrapy, pyspark
```

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
```

This starts:

- **Zookeeper** (port 2181)
- **Kafka broker** (port 9092)
- **Schema Registry** (port 8081)
- **Confluent Control Center** (port 9021) — UI for topics and consumers
- **Spark Master** (UI: 9090, driver: 7077)
- **Spark Worker**

### 2. Run the crawler

From the project root, with Kafka running and listening on `localhost:9092`:

```bash
cd crawler
scrapy crawl itviec
```

Scraped items are sent to the Kafka topic `itviec`.

### 3. Run the Spark streaming job

The Spark job reads from the `itviec` topic, applies the schema, extracts skills, and writes to PostgreSQL. Run it inside the Spark cluster (e.g. submit from the `spark-master` container) or adapt for your Spark deployment. Ensure PostgreSQL is reachable (e.g. `host.docker.internal:5432`) and the database `jobdb` and staging schema/tables exist.

Example (from host, if Spark is configured to accept submissions):

```bash
# Example: submit from spark-master container
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-jobs/spark_stream.py
```

Adjust paths and master URL to match your setup.

## Configuration

- **Kafka (crawler)**: `pipelines.py` uses `bootstrap_servers=['localhost:9092']`. Use the same for local runs; in Docker use the service name (e.g. `broker:29092`).
- **Kafka (Spark)**: `spark_stream.py` uses `broker:29092` (Docker network).
- **PostgreSQL**: In `spark_stream.py`, JDBC URL, user, password, and table names are set for `host.docker.internal` and schema `staging`. Create the database and tables (jobs, companies, skills, job_skills, locations, job_locations) as needed.

## Tech Stack

| Component   | Technology        |
|------------|-------------------|
| Crawling   | Scrapy 2.11       |
| Messaging  | Apache Kafka      |
| Processing | PySpark 3.4 (Structured Streaming) |
| Storage    | PostgreSQL (staging) |
| Runtime    | Docker, Confluent platform, Apache Spark |

## License

See repository for license information.
