"""Tests for query measurements_of_interest_summary.sql.

See https://github.com/verilylifesciences/analysis-py-utils for more details
about the testing framework.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ddt import ddt
import os
import unittest
from verily.bigquery_wrapper import bq_test_case

SQL_TEMPLATE = "measurements_of_interest_summary.sql"


@ddt
class QueryTest(bq_test_case.BQTestCase):

  @classmethod
  def setUpClass(cls):
    """Set up class."""
    super(QueryTest, cls).setUpClass(use_mocks=False)
    cls.sql_to_test = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     SQL_TEMPLATE), "r").read()

  @classmethod
  def create_mock_tables(cls):
    """Create mock tables."""

    cls.client.create_table_from_query("""
SELECT * FROM UNNEST([
STRUCT<concept_id INT64,
       concept_name STRING>
    (123, 'Hemoglobin'),
    (456, 'gram per deciliter')
])
    """, cls.client.path("concept"))

    cls.client.create_table_from_query("""
SELECT * FROM UNNEST([
STRUCT<measurement_concept_id INT64,
       unit_concept_id INT64,
       operator_concept_id INT64,
       value_as_number FLOAT64,
       value_as_concept_id INT64>
    (123, 456, NULL, 42.0, NULL),
    (123, 456, NULL, 13.5, NULL),
    (123, 456, NULL, NULL, 100),
    (123, 456, NULL, NULL, NULL),
    (123, 456, 789, 7.2, NULL)
])
    """, cls.client.path("measurement"))

    # Get the project id and dataset name where the temp tables are stored.
    (project_id, dataset_id, _) = cls.client.parse_table_path(
        cls.client.path("any_temp_table"))
    cls.src_dataset = ".".join([project_id, dataset_id])

  def test(self):
    sql = self.sql_to_test.format(
        CDR=self.src_dataset,
        MEASUREMENT_OF_INTEREST="hemoglobin")

    expected = [
        # measurement	unit	N	missing	min	max	avg	stddev	quantiles	num_numeric_values	num_concept_values	num_operators	measurement_concept_id	unit_concept_id
        ("Hemoglobin", "gram per deciliter", 5, 1, 7.2, 42.0, 20.9, 18.542653531789888, [7.2, 7.2, 13.5, 42.0, 42.0], 3, 1, 1, 123, 456)
        ]
    self.expect_query_result(query=sql, expected=expected)

if __name__ == "__main__":
  unittest.main()

