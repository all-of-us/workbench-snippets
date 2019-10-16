
-- Compute the count of all unique participants in All of Us
-- that have at least one measurement.
SELECT
  COUNT(DISTINCT person_id) AS number_of_participants_with_measurements
FROM
  `{CDR}.measurement`
