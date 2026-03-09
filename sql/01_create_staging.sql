-- Create staging schema and tables (raw data from Spark pipeline)

CREATE SCHEMA staging;

CREATE TABLE staging.jobs (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    company TEXT,
    salary TEXT,
    url TEXT,
    locations TEXT[],
    batch_id BIGINT
);

CREATE TABLE staging.companies (
    id BIGSERIAL PRIMARY KEY,
    company TEXT,
    batch_id BIGINT
);

CREATE TABLE staging.skills (
    id BIGSERIAL PRIMARY KEY,
    skill TEXT,
    batch_id BIGINT
);

CREATE TABLE staging.job_skills (
    id BIGSERIAL PRIMARY KEY,
    url TEXT,
    skill TEXT,
    batch_id BIGINT
);

CREATE TABLE staging.locations (
    id BIGSERIAL PRIMARY KEY,
    location TEXT,
    batch_id BIGINT
);

CREATE TABLE staging.job_locations (
    id BIGSERIAL PRIMARY KEY,
    url TEXT,
    location TEXT,
    batch_id BIGINT
);
