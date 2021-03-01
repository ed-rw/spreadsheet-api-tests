"""
Tests for the endpoints pertaining to view spreadsheet endpoint
"""

import pytest
import requests

from const import SERVICE_BASE_URL
from utils import new_spreadsheet_fixture, create_cell


# This class comes first since the tests for the cells collection endpoint
# depends on being able to create cells
class TestViewSpreadsheetEndpoint:

    def test_view_non_existant_spreadsheet(self):
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                            "/view")

        assert resp.status_code == 404

    def test_view_empty_spreadsheet(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                           f"/{spreadsheet_id}/view")

        assert resp.status_code == 200
        assert resp.content.decode("utf-8") == ""

    def test_view_spreadsheet(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']
        create_cell(spreadsheet_id, "A1", "a1")
        create_cell(spreadsheet_id, "B2", "b2")
        create_cell(spreadsheet_id, "D5", "d5")

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                           f"/{spreadsheet_id}/view")

        assert resp.status_code == 200

        assert (resp.content.decode("utf-8")
                == "*\tA\tB\tC\tD\n1\ta1\t\t\t\n2\t\tb2\t\t\n3\t\t\t\t\n"
                   "4\t\t\t\t\n5\t\t\t\td5")
