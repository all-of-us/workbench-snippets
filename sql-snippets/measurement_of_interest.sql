
-- Return row level data for a measurement for our cohort.
--
-- PARAMETERS:
--   MEASUREMENT_CONCEPT_ID: for example 3004410        # Hemoglobin A1c
--   UNIT_CONCEPT_ID: for example 8554                  # percent

WITH
  --
  -- Retrieve participants birthdate and sex_at_birth.
  --
persons AS (
  SELECT
    person_id,
    birth_datetime,
    concept_name AS sex_at_birth
  FROM
    `{CDR}.person`
  LEFT JOIN `{CDR}.concept` ON concept_id = sex_at_birth_concept_id),
  --
  -- Retrieve the row-level data for our measurement of interest.
  --
measurements AS (
  SELECT
    person_id,
    measurement_id,
    measurement_concept_id,
    measurement_date,
    measurement_datetime,
    measurement_type_concept_id,
    operator_concept_id,
    value_as_number,
    value_as_concept_id,
    unit_concept_id,
    range_low,
    range_high
  FROM
    `{CDR}.measurement`
  WHERE
    measurement_concept_id = {MEASUREMENT_CONCEPT_ID}
    AND unit_concept_id = {UNIT_CONCEPT_ID}
    AND person_id IN ({COHORT_QUERY}))
  --
  -- Lastly, JOIN all this data together so that we have the birthdate, sex_at_birth and site for each measurement.
  --
SELECT
  persons.*,
  src_id,
  measurements.* EXCEPT(person_id, measurement_id)
FROM
  measurements
LEFT JOIN
  persons USING (person_id)
LEFT JOIN
  `{CDR}.measurement_ext` USING (measurement_id)
ORDER BY
  person_id,
  measurement_id

