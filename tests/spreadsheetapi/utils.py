"""
Utility classes and functions for the tests.
"""

import pytest
import requests

from const import SERVICE_BASE_URL

def create_cell(spreadsheet_id, cell_name, cell_value):
    resp = requests.put(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                        f"/{spreadsheet_id}/cells/{cell_name}",
                        json={'value': cell_value, 'type': 'literal'})
    return resp


def delete_cell(spreadsheet_id, cell_name):
    resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets"
                           f"/{spreadsheet_id}/cells/{cell_name}")
    return resp


class SpreadsheetCreationManager:

    def __init__(self):
        self.created_spreadsheets = {}

    def __call__(self, name):
        if name in self.created_spreadsheets:
            return self.created_spreadsheets[name]
        else:
            resp = requests.post(f"{SERVICE_BASE_URL}/v1/spreadsheets",
                                 json={'name': name})
            resp.raise_for_status()
            self.created_spreadsheets[name] = resp
            return resp

    def delete_resources(self):
        for _, resp in self.created_spreadsheets.items():
            spreadsheet_id = resp.json()['id']
            print(f"DELETING SPREADSHEET: {spreadsheet_id}")
            resp = requests.delete(f"{SERVICE_BASE_URL}/v1/spreadsheets/{spreadsheet_id}")
            resp.raise_for_status()


@pytest.fixture(scope="class")
def new_spreadsheet_fixture():
    manager = SpreadsheetCreationManager()

    yield manager

    manager.delete_resources()
