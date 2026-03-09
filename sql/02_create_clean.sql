-- Create clean schema and tables (normalized for analytics)

CREATE SCHEMA clean;

CREATE TABLE clean.companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE clean.skills (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE clean.locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE clean.jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    salary TEXT,
    url TEXT NOT NULL UNIQUE,
    company_id INTEGER REFERENCES clean.companies(id) ON DELETE SET NULL
);

CREATE TABLE clean.job_skills (
    job_id INTEGER REFERENCES clean.jobs(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES clean.skills(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);

CREATE TABLE clean.job_locations (
    job_id INTEGER REFERENCES clean.jobs(id) ON DELETE CASCADE,
    location_id INTEGER REFERENCES clean.locations(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, location_id)
);

CREATE TABLE clean.job_levels (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE clean.job_roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE clean.job_level_map (
    job_id INT REFERENCES clean.jobs(id) ON DELETE CASCADE,
    level_id INT REFERENCES clean.job_levels(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, level_id)
);

CREATE TABLE clean.job_role_map (
    job_id INT REFERENCES clean.jobs(id) ON DELETE CASCADE,
    role_id INT REFERENCES clean.job_roles(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, role_id)
);
