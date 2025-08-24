import os
import sys
import pytest
import chromedriver_autoinstaller
from dash.testing.application_runners import import_app

# Add the project root (one level up from tests/) to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Auto-install ChromeDriver
chromedriver_autoinstaller.install()


@pytest.fixture
def dash_app(dash_duo):
    # Now this should find app.py
    app = import_app("app")
    dash_duo.start_server(app)
    return dash_duo


def test_header_present(dash_app):
    header = dash_app.find_element("#header")
    assert header is not None
    assert "Pink Morsel Sales" in header.text


def test_visualisation_present(dash_app):
    graph = dash_app.find_element("#sales-graph")
    assert graph is not None


def test_region_picker_present(dash_app):
    region_picker = dash_app.find_element("#region-picker")
    assert region_picker is not None
