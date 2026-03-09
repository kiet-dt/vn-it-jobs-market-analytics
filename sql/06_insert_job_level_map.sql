-- Map jobs to levels by title keywords (run after 03, 04)
-- Adds unique constraint then inserts level mappings.

ALTER TABLE clean.job_level_map
ADD CONSTRAINT job_level_unique UNIQUE (job_id, level_id);

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Intern'
WHERE j.title ILIKE '%intern%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Fresher'
WHERE j.title ILIKE '%fresher%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Junior'
WHERE
    j.title ILIKE '%junior%'
    OR j.title ILIKE '%jr%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Middle'
WHERE
    j.title ILIKE '%middle%'
    OR j.title ILIKE '%mid%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Senior'
WHERE
    j.title ILIKE '%senior%'
    OR j.title ILIKE '%sr%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Lead'
WHERE
    j.title ILIKE '%lead%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_level_map (job_id, level_id)
SELECT j.id, l.id
FROM clean.jobs j
JOIN clean.job_levels l ON l.name = 'Other'
WHERE NOT EXISTS (
    SELECT 1
    FROM clean.job_level_map m
    WHERE m.job_id = j.id
);
