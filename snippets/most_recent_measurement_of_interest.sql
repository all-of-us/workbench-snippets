
-- Return row level data for a measurement, limited to only the most recent result per person.
--
-- PARAMETERS:
--   MEASUREMENT_CONCEPT_ID: for example 3000963  # Hemoglobin
--   UNIT_CONCEPT_ID: for example 8713            # gram per deciliter

WITH
  --
  -- Retrieve participants birthdate and gender.
  --
persons AS (
  SELECT
    person_id,
    birth_datetime,
    concept_name AS gender
  FROM
    `{CDR}.person`
  LEFT JOIN `{CDR}.concept` ON concept_id = gender_concept_id),
  --
  -- Retrieve the row-level data for our measurement of interest. Also compute
  -- a new column for the recency rank of the measurement per person, a rank of
  -- of 1 being the most recent lab result for that person.
  --
measurements AS (
  SELECT
    person_id,
    measurement_id,
    measurement_concept_id,
    unit_concept_id,
    measurement_date,
    measurement_datetime,
    measurement_type_concept_id,
    operator_concept_id,
    value_as_number,
    value_as_concept_id,
    range_low,
    range_high,
    ROW_NUMBER() OVER (PARTITION BY person_id
                       ORDER BY measurement_date DESC,
                                measurement_datetime DESC,
                                measurement_id DESC) AS recency_rank

  FROM
    `{CDR}.measurement`
  WHERE
    measurement_concept_id = {MEASUREMENT_CONCEPT_ID} AND unit_concept_id = {UNIT_CONCEPT_ID}),
  --
  -- Get the human-readable names for the site from which the measurement came.
  --
sites AS (
  SELECT
    measurement_id,
    src_id
  FROM
    `{CDR}.measurement_ext`
  GROUP BY  # This GROUP BY is here to deal with duplicate rows in the R2019Q1R2 release of the table.
    1, 2)
  --
  -- Lastly, JOIN all this data together so that we have the birthdate, gender and site for each
  -- measurement, retaining only the most recent result per person.
  --
SELECT
  persons.*,
  sites.src_id,
  measurements.* EXCEPT(person_id, measurement_id, recency_rank)
FROM
  measurements
LEFT JOIN
  persons USING (person_id)
LEFT JOIN
  sites USING (measurement_id)
WHERE
  recency_rank = 1
ORDER BY
  person_id,
  measurement_id

