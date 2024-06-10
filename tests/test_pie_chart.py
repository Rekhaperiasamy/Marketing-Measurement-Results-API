from unittest.mock import MagicMock

from database.models import MarketingData


MOCK_DATA = [
    ('Channel1', 1481465.83601774657939947531),
    ('Channel2', 185975.5927779741463644024),
    ('Channel3', 1467253.57685746059446818013),
    ('Channel4', 2478040.2239182248721135048)
]


def test_show_pie_chart(test_client, mock_db_session, mock_get_marketing_data_filter):
    # Set up the mock objects
    mock_get_marketing_data_filter.return_value = []

    # Mock the query and all() method
    mock_query = MagicMock()
    mock_query.filter.return_value.group_by.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    response = test_client.get("/pie-chart")

    total_value = sum(value for _, value in MOCK_DATA)
    expected_response = [
        {
            "channel": "Channel1",
            "net_sales": 1481465.83601774657939947531,
            "percentage": (1481465.83601774657939947531 / total_value) * 100
        },
        {
            "channel": "Channel2",
            "net_sales": 185975.5927779741463644024,
            "percentage": (185975.5927779741463644024 / total_value) * 100
        },
        {
            "channel": "Channel3",
            "net_sales": 1467253.57685746059446818013,
            "percentage": (1467253.57685746059446818013 / total_value) * 100
        },
        {
            "channel": "Channel4",
            "net_sales": 2478040.2239182248721135048,
            "percentage": (2478040.2239182248721135048 / total_value) * 100
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected_response


def test_show_pie_chart_with_filters(test_client, mock_db_session, mock_get_marketing_data_filter):
    # Set up the mock objects with filters
    mock_get_marketing_data_filter.return_value = ["filter_expression"]

    # Mock the query and all() method
    mock_query = MagicMock()
    mock_query.filter.return_value.group_by.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    params = {
        "product": "Product1",
        "campaign_type": "Type1",
        "campaign": "Campaign1",
        "channel": "Channel1",
        "start_date": "2023-01-01",
        "end_date": "2023-01-02"
    }

    response = test_client.get("/pie-chart", params=params)

    total_value = sum(value for _, value in MOCK_DATA)
    expected_response = [
        {
            "channel": "Channel1",
            "net_sales": 1481465.83601774657939947531,
            "percentage": (1481465.83601774657939947531 / total_value) * 100
        },
        {
            "channel": "Channel2",
            "net_sales": 185975.5927779741463644024,
            "percentage": (185975.5927779741463644024 / total_value) * 100
        },
        {
            "channel": "Channel3",
            "net_sales": 1467253.57685746059446818013,
            "percentage": (1467253.57685746059446818013 / total_value) * 100
        },
        {
            "channel": "Channel4",
            "net_sales": 2478040.2239182248721135048,
            "percentage": (2478040.2239182248721135048 / total_value) * 100
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected_response
    mock_get_marketing_data_filter.assert_called_once_with(
        MarketingData, "Product1", "Type1", "Campaign1", "Channel1", "2023-01-01", "2023-01-02")
    mock_query.filter.assert_called_once_with("filter_expression")
