
-- Compute the count of all unique participants in AoU
-- that have at least one condition.
SELECT
  COUNT(DISTINCT person_id) AS number_of_participants_with_med_conditions
FROM
  `{DATASET}.condition_occurrence`

