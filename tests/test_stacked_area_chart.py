from unittest.mock import MagicMock

from database.models import MarketingData


MOCK_DATA = [
    ("Channel1", "2023-01-01", 100),
    ("Channel2", "2023-01-01", 200),
    ("Channel1", "2023-01-02", 150),
    ("Channel2", "2023-01-02", 250),
]


def test_show_stacked_area_chart(test_client, mock_db_session, mock_get_marketing_data_filter):
    # Set up the mock objects
    mock_get_marketing_data_filter.return_value = []

    # Mock the query and all() method
    mock_query = MagicMock()
    mock_query.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    response = test_client.get("/stacked-area-chart")

    expected_response = [
        {"channel": "Channel1", "date": "2023-01-01", "net_sales": 100},
        {"channel": "Channel2", "date": "2023-01-01", "net_sales": 200},
        {"channel": "Channel1", "date": "2023-01-02", "net_sales": 150},
        {"channel": "Channel2", "date": "2023-01-02", "net_sales": 250},
    ]

    assert response.status_code == 200
    assert response.json() == expected_response


def test_show_stacked_area_chart_with_filters(test_client, mock_db_session, mock_get_marketing_data_filter):
    # Set up the mock objects with filters
    mock_get_marketing_data_filter.return_value = ["filter_expression"]

    # Mock the query and all() method
    mock_query = MagicMock()
    mock_query.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    params = {
        "product": "Product1",
        "campaign_type": "Type1",
        "campaign": "Campaign1",
        "channel": "Channel1",
        "start_date": "2023-01-01",
        "end_date": "2023-01-02"
    }

    response = test_client.get("/stacked-area-chart", params=params)

    expected_response = [
        {"channel": "Channel1", "date": "2023-01-01", "net_sales": 100},
        {"channel": "Channel2", "date": "2023-01-01", "net_sales": 200},
        {"channel": "Channel1", "date": "2023-01-02", "net_sales": 150},
        {"channel": "Channel2", "date": "2023-01-02", "net_sales": 250},
    ]

    assert response.status_code == 200
    assert response.json() == expected_response
    mock_get_marketing_data_filter.assert_called_once_with(
        MarketingData, "Product1", "Type1", "Campaign1", "Channel1", "2023-01-01", "2023-01-02")
    mock_query.filter.assert_called_once_with("filter_expression")
