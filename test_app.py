
import pytest
from dash.testing.application_runners import import_app

# Load the Dash app from app.py
@pytest.fixture
def dash_app():
    app = import_app("app")  # imports app.py
    return app

def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("#header-title")
    assert header is not None
    assert "Pink Morsel Sales" in header.text

def test_graph_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-graph")
    assert graph is not None

def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    picker = dash_duo.find_element("#region-radio")
    assert picker is not None
