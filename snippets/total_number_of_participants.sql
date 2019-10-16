
-- Compute the count of all unique participants in AoU.
SELECT
  COUNT(DISTINCT person_id) AS total_number_of_participants
FROM
  `{CDR}.person`

