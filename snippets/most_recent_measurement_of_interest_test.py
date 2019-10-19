"""Tests for query most_recent_measurement_of_interest.sql.

See https://github.com/verilylifesciences/analysis-py-utils for more details
about the testing framework.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import date
from datetime import datetime
from dateutil import tz
from ddt import ddt
import os
import unittest
from verily.bigquery_wrapper import bq_test_case

SQL_TEMPLATE = "most_recent_measurement_of_interest.sql"


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
STRUCT<person_id INT64,
       birth_datetime TIMESTAMP,
       gender_concept_id INT64>
    (1001, '1990-12-31 00:00:00 UTC', 501),
    (1002, '1950-08-01 00:00:00 UTC', 500),
    (1003, '1965-06-30 00:00:00 UTC', 500)
])
    """, cls.client.path("person"))

    cls.client.create_table_from_query("""
SELECT * FROM UNNEST([
STRUCT<concept_id INT64,
       concept_name STRING,
       vocabulary_id STRING>
    (  0, 'No matching concept', 'None'),
    (123, 'Hemoglobin', 'LOINC'),
    (456, 'gram per deciliter', 'UCUM'),
    (500, 'FEMALE', 'Gender'),
    (501, 'MALE', 'Gender')
])
    """, cls.client.path("concept"))

    cls.client.create_table_from_query("""
SELECT * FROM UNNEST([
STRUCT<measurement_id INT64,
       src_id STRING>
    (1, 'site1'),
    (2, 'site1'),
    (3, 'site1'),
    (4, 'site2'),
    (5, 'site2')
])
    """, cls.client.path("measurement_ext"))

    cls.client.create_table_from_query("""
SELECT * FROM UNNEST([
STRUCT<measurement_id INT64,
       person_id INT64,
       measurement_source_concept_id INT64,
       measurement_concept_id INT64,
       unit_concept_id INT64,
       operator_concept_id INT64,
       measurement_date DATE,
       measurement_datetime TIMESTAMP,
       measurement_type_concept_id INT64,
       value_as_number FLOAT64,
       value_as_concept_id INT64,
       range_low FLOAT64,
       range_high FLOAT64>
    (1, 1001, 123, 123, 456, NULL, '2005-12-31', '2005-12-31 10:30:00 UTC', NULL, 42.0, NULL, 0, 999),
    (2, 1001, 123, 123, 456, NULL, '2007-09-11', '2007-09-11 08:00:00 UTC', NULL, 13.5, NULL, 0, 999),
    (3, 1001, 123, 123, 456, NULL, '2007-09-11', '2007-09-11 20:59:00 UTC', NULL, NULL,  100, 0, 999),
    (4, 1002, 123, 123, 456, NULL, '2008-02-10', '2008-02-10 23:30:00 UTC', NULL, NULL, NULL, 0, 999),
    (5, 1002, 123, 123, 456,  789, '2008-02-10', '2008-02-10 23:30:00 UTC', NULL,  7.2, NULL, 0, 999),
    # This measurement is for someone not in our cohort.
    (6, 1003, 123, 123, 456,  789, '2010-01-01', '2010-10-01 23:30:00 UTC', NULL,  500, NULL, 0, 999)
])
    """, cls.client.path("measurement"))

    # Get the project id and dataset name where the temp tables are stored.
    (project_id, dataset_id, _) = cls.client.parse_table_path(
        cls.client.path("any_temp_table"))
    cls.src_dataset = ".".join([project_id, dataset_id])

  def test(self):
    sql = self.sql_to_test.format(
        CDR=self.src_dataset,
        COHORT_QUERY="SELECT person_id FROM `{}.person` WHERE person_id <= 1002".format(self.src_dataset),
        MEASUREMENT_CONCEPT_ID=123,
        UNIT_CONCEPT_ID=456)

    expected = [
        # person_id	birth_datetime	gender	src_id	measurement_concept_id	unit_concept_id	measurement_date	measurement_datetime	measurement_type_concept_id	operator_concept_id	value_as_number	value_as_concept_id	range_low	range_high measurement_source
        (1001, datetime(1990, 12, 31, 0, 0, tzinfo=tz.gettz("UTC")),  "MALE", "site1", 123, 456, date(2007, 9, 11), datetime(2007, 9, 11, 20, 59, tzinfo=tz.gettz("UTC")), None, None, None,  100, 0, 999, "EHR"),
        (1002, datetime(1950, 8, 1, 0, 0, tzinfo=tz.gettz("UTC")),  "FEMALE", "site2", 123, 456, date(2008, 2, 10), datetime(2008, 2, 10, 23, 30, tzinfo=tz.gettz("UTC")), None,  789,  7.2, None, 0, 999, "EHR")
        ]
    self.expect_query_result(query=sql, expected=expected)

if __name__ == "__main__":
  unittest.main()

