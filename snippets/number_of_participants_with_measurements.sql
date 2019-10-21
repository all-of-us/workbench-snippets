
-- Compute the count of unique participants in our All of Us cohort
-- that have at least one measurement.
SELECT
  COUNT(DISTINCT person_id) AS number_of_participants_with_measurements
FROM
  `{CDR}.measurement`
WHERE
  person_id IN ({COHORT_QUERY})
