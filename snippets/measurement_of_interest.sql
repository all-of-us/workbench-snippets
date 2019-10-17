
-- Return row level data for a measurement.
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
  -- Lastly, JOIN all this data together so that we have the birthdate, gender and site for each measurement.
  --
SELECT
  persons.*,
  sites.src_id,
  measurements.* EXCEPT(person_id, measurement_id)
FROM
  measurements
LEFT JOIN
  persons USING (person_id)
LEFT JOIN
  sites USING (measurement_id)
ORDER BY
  person_id,
  measurement_id

