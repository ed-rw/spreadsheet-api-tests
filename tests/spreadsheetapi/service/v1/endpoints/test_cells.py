"""
Tests for the endpoints pertaining to cell resources.
"""

import pytest
import requests

from const import SERVICE_BASE_URL
from utils import new_spreadsheet_fixture


def create_cell(spreadsheet_id, cell_name, cell_value):
    resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                        f"/{spreadsheet_id}/cells/{cell_name}",
                        json={'value': cell_value, 'type': 'literal'})
    return resp


def delete_cell(spreadsheet_id, cell_name):
    resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                           f"/{spreadsheet_id}/cells/{cell_name}")
    return resp


@pytest.fixture(scope="class")
def cells_from_A1_to_D4_fixture(new_spreadsheet_fixture):
    new_spreadsheet_resp = new_spreadsheet_fixture("new_spreadsheet")
    spreadsheet_id = new_spreadsheet_resp.json()['id']

    for col in ('A', 'B', 'C', 'D'):
        for row in range(1, 5):
            cell_name = f"{col}{row}"
            resp = create_cell(spreadsheet_id, cell_name, f"dummy value {cell_name}")
            resp.raise_for_status()

    yield new_spreadsheet_resp

    # Remove cells
    for col in ('A', 'B', 'C', 'D'):
        for row in range(1, 5):
            cell_name = f"{col}{row}"
            resp = delete_cell(spreadsheet_id, cell_name)
            resp.raise_for_status()

# This class comes first since the tests for the cells collection endpoint
# depends on being able to create cells
class TestCellEndpoint:

    def test_get_cell_404(self):
        """Try to get a cell for a non-existant spreadsheet"""
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                           f"/cells/A1")

        assert resp.status_code == 404

    def test_get_cell_null(self, new_spreadsheet_fixture):
        """Try to get a cell that has not had a value set yet"""

        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                           f"/{spreadsheet_id}/cells/A1")

        assert resp.status_code == 200
        assert resp.json() == None

    def test_create_cell_404(self):

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                             f"/cells/A1",
                             json={'value': 'dummy value', 'type': 'literal'})

        assert resp.status_code == 404

    def test_create_cell_422_invalid_name_A0(self):

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                             f"/cells/A0",
                             json={'value': 'dummy value', 'type': 'literal'})

        assert resp.status_code == 422

    def test_create_cell_422_invalid_name_1B(self):

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                             f"/cells/1B",
                             json={'value': 'dummy value', 'type': 'literal'})

        assert resp.status_code == 422

    def test_create_cell_422_invalid_type(self):

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                             f"/cells/1B",
                             json={'value': 'dummy value', 'type': 'badtype'})

        assert resp.status_code == 422

    def test_create_cell(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                             f"/{spreadsheet_id}/cells/A1",
                             json={'value': 'dummy value', 'type': 'literal'})

        assert resp.status_code == 200

    def test_get_cell_200(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                             f"/{spreadsheet_id}/cells/A1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert resp_data['name'] == "A1"
        assert resp_data['data']['value'] == "dummy value"
        assert resp_data['data']['type'] == "literal"

    def test_update_cell_200(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                             f"/{spreadsheet_id}/cells/A1",
                             json={'value': 'dummy value update', 'type': 'literal'})

    def test_get_updated_cell_200(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                             f"/{spreadsheet_id}/cells/A1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert resp_data['name'] == "A1"
        assert resp_data['data']['value'] == "dummy value update"
        assert resp_data['data']['type'] == "literal"

    def test_delete_cell_404(self):

        resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets/doesnt_exist"
                             f"/cells/A1")

        assert resp.status_code == 404

    def test_delete_cell_existing(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                               f"/{spreadsheet_id}/cells/A1")

        assert resp.status_code == 200

    def test_delete_cell_non_existing(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                               f"/{spreadsheet_id}/cells/A1")

        assert resp.status_code == 200

class TestCellsEndpoint:

    def test_get_cells_no_cells(self, new_spreadsheet_fixture):
        spreadsheet_id = new_spreadsheet_fixture("new_spreadsheet").json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/"
                            f"{spreadsheet_id}/cells")

        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_cells_404(self):
        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/"
                            f"doesnt_exist/cells")

        assert resp.status_code == 404

    def test_get_cells_with_cells(self, cells_from_A1_to_D4_fixture):
        # NOTE: This is is a little woinky, the cells fixture just returns
        # the same thing as new_spreadsheet_fixture. Making dataclasses to
        # return here could prove more elegant
        spreadsheet_id = cells_from_A1_to_D4_fixture.json()['id']

        resp = requests.get(f"{SERVICE_BASE_URL}/v1/spreadsheets/"
                            f"{spreadsheet_id}/cells")
        resp_data = resp.json()

        assert resp.status_code == 200

        assert len(resp_data) == 16
        # Check that the cell names we expect to exist are in the set of cells
        # returned from the call
        cell_names_set = {e['name'] for e in resp_data}
        for col in ('A', 'B', 'C', 'D'):
            for row in range(1, 5):
                assert f"{col}{row}" in cell_names_set

        # Check for consistency of data in cells
        for cell in resp_data:
            assert cell['data']['value'] == f"dummy value {cell['name']}"
            assert cell['data']['type'] == "literal"
