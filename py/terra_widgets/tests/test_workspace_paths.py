"""Tests for the WorkspacePaths class."""

import os
import unittest
from terra_widgets.workspace_paths import WorkspacePaths


class TestWorkspacePaths(unittest.TestCase):

  def setUp(self):
    self.wp = WorkspacePaths(workspace_bucket='fc-fake-bucket')
    os.environ['OWNER_EMAIL'] = 'testUser@somecompany.com'

  def tearDown(self):
    os.unsetenv('OWNER_EMAIL')

  def test_destinations(self):
    notebook_paths = ['gs://fc-fake-bucket/notebooks/test1.ipynb',
                      'gs://fc-fake-bucket/notebooks/test2.ipynb']
    destinations = self.wp.formulate_destination_paths(notebooks=notebook_paths)
    self.assertSetEqual(set(destinations.keys()), set(notebook_paths))
    self.assertRegex(
        destinations[notebook_paths[0]].html_file,
        r'gs://fc-fake-bucket/reports/testUser@somecompany.com/\d{8}/\d{6}/test1.html')
    self.assertRegex(
        destinations[notebook_paths[0]].comment_file,
        r'gs://fc-fake-bucket/reports/testUser@somecompany.com/\d{8}/\d{6}/test1.comment.txt')
    self.assertRegex(
        destinations[notebook_paths[1]].html_file,
        r'gs://fc-fake-bucket/reports/testUser@somecompany.com/\d{8}/\d{6}/test2.html')
    self.assertRegex(
        destinations[notebook_paths[1]].comment_file,
        r'gs://fc-fake-bucket/reports/testUser@somecompany.com/\d{8}/\d{6}/test2.comment.txt')

  def test_fail_destinations(self):
    with self.assertRaisesRegex(
        ValueError,
        r'"gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/120000/test1.html" does not match "gs://fc-fake-bucket/notebooks/\*\.ipynb"'):
      self.wp.formulate_destination_paths(notebooks=['gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/120000/test1.html'])

  def test_glob_for_aou(self):
    input_path = 'gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/120000'
    expected = os.path.join(input_path, '*.html')
    self.assertEqual(self.wp.add_html_glob_to_path(input_path), expected)

  def test_glob_for_terra(self):
    wp = WorkspacePaths(workspace_bucket='fc-fake-bucket')
    input_path = 'gs://fc-fake-bucket/reports/test@somecompany.com/20200701/120000'
    expected = os.path.join(input_path, '*.html')
    self.assertEqual(wp.add_html_glob_to_path(input_path), expected)

  def test_glob_path_already_complete(self):
    # Pass a complete path to an HTML file when instead we should pass a partial path to it.
    with self.assertRaisesRegex(ValueError, '"gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/120000/test1.html" does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/120000/test1.html')

  def test_glob_path_missing_time(self):
    with self.assertRaisesRegex(ValueError, 'does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/reports/test@researchallofus.org/20200701/')

  def test_glob_path_missing_date(self):
    with self.assertRaisesRegex(ValueError, 'does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/reports/test@researchallofus.org/120000/')

  def test_glob_path_missing_user(self):
    with self.assertRaisesRegex(ValueError, 'does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/reports/20200701/120000/')

  def test_glob_path_missing_report_folder(self):
    with self.assertRaisesRegex(ValueError, 'does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/test@researchallofus.org/20200701/120000/')

  def test_glob_wrong_path(self):
    # Pass a path to a notebook when instead we should pass a partial path to a report.
    with self.assertRaisesRegex(ValueError, '"gs://fc-fake-bucket/notebooks/test1.ipynb" does not match'):
      self.wp.add_html_glob_to_path('gs://fc-fake-bucket/notebooks/test1.ipynb')


if __name__ == '__main__':
  unittest.main()

