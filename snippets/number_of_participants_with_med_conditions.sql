
-- Compute the count of unique participants in our All of Us cohort
-- that have at least one condition.
SELECT
  COUNT(DISTINCT person_id) AS number_of_participants_with_med_conditions
FROM
  `{CDR}.condition_occurrence`
WHERE
  person_id IN ({COHORT_QUERY})
