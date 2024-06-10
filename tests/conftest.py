# test_app.py

import pytest
from fastapi.testclient import TestClient
from main import app

from unittest.mock import patch


@pytest.fixture
def test_client():
    yield TestClient(app)


@pytest.fixture
def mock_db_session():
    with patch("routers.marketing.db_session") as mock:
        yield mock


@pytest.fixture
def mock_get_marketing_data_filter():
    with patch("routers.marketing.Filters.get_marketing_data_filter") as mock:
        yield mock
