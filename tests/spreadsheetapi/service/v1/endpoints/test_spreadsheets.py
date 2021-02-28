"""
Tests for the endpoints pertaining to spreadsheet resources.
"""

import pytest
import requests

from const import SERVICE_BASE_URL
from utils import new_spreadsheet_fixture


class TestSpreadsheetsEndpoint:

    def test_create_first_spreadsheet(self, new_spreadsheet_fixture):
        resp = new_spreadsheet_fixture("first_test_spreadsheet")
        spreadsheet_id = resp.json()['id']

        assert resp.status_code == 201
        # TODO assert id returned is uuid

    def test_get_spreadsheets_with_one_spreadsheet(self):
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets")
        resp_data = resp.json()

        assert "first_test_spreadsheet" in {e['name'] for e in resp_data}

    def test_get_spreadsheets_with_two_spreadsheets(self, new_spreadsheet_fixture):
        # First spreadsheet created still exists since new_spreadsheet_fixture
        # is scoped to the class
        resp = new_spreadsheet_fixture("second_test_spreadsheet")

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets")
        resp_data = resp.json()

        # Check that the set of names we expect is in the set of current
        # spreadsheet names
        assert set(["first_test_spreadsheet", "second_test_spreadsheet"]).issubset(
                {e['name'] for e in resp_data})

    # QUESTION: How to delete the spreadsheets created here... would be nice
    # to have this series of tests clean up after itself.


class TestSpreadsheetEndpoint:

    def test_get_200(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/{spreadsheet_id}")
        resp_data = resp.json()

        assert resp_data['id'] == spreadsheet_id
        assert resp_data['name'] == "new_spreadsheet"

    def test_get_404(self):
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist")

        assert resp.status_code == 404

    def test_update_200(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']
        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/{spreadsheet_id}",
                            json={'name': "new_spreadsheet_name"})

        assert resp.status_code == 200
        assert resp.json()['id'] == spreadsheet_id

    def test_get_200_new_name(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/{spreadsheet_id}")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert resp_data['id'] == spreadsheet_id
        assert resp_data['name'] == "new_spreadsheet_name"

    def test_update_404(self):
        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist",
                            json={'name': "new_name"})

        assert resp.status_code == 404

    def test_delete_existing(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']
        resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets/{spreadsheet_id}")

        assert resp.status_code == 200

    def tests_delete_non_existing(self):
        resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist")

        assert resp.status_code == 200
