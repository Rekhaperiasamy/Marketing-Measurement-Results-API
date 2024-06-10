# test_app.py
from unittest.mock import MagicMock

from database.models import MarketingData


MOCK_DATA = [
    MarketingData(id=1, product="Product1", campaign_type="Type1",
                  campaign="Campaign1", channel="Channel1", date="2023-01-01", conversions=664.1394510189357),
    MarketingData(id=2, product="Product2", campaign_type="Type2",
                  campaign="Campaign2", channel="Channel2", date="2023-01-02", conversions=82.07983229688519),
]


def test_marketing_data_endpoint_without_filter(test_client, mock_db_session, mock_get_marketing_data_filter):
    mock_get_marketing_data_filter.return_value = []

    mock_query = MagicMock()
    # mock_query.filter.return_value.all.return_value = MOCK_DATA
    mock_query.filter.return_value.limit.return_value.offset.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    response = test_client.get("/marketing-data")

    assert response.status_code == 200
    assert response.json() == [
        {
            "product": "Product1",
            "campaign_type": "Type1",
            "campaign": "Campaign1",
            "channel": "Channel1",
            "date": "2023-01-01",
            "conversions": 664.1394510189357
        },
        {
            "product": "Product2",
            "campaign_type": "Type2",
            "campaign": "Campaign2",
            "channel": "Channel2",
            "date": "2023-01-02",
            "conversions": 82.07983229688519
        }
    ]


def test_read_marketing_data_with_filters(test_client, mock_db_session, mock_get_marketing_data_filter):
    # Set up the mock objects with filters
    mock_get_marketing_data_filter.return_value = ["filter_expression"]

    # Mock the query and all() method
    mock_query = MagicMock()
    # mock_query.filter.return_value.all.return_value = MOCK_DATA
    mock_query.filter.return_value.limit.return_value.offset.return_value.all.return_value = MOCK_DATA
    mock_db_session.query.return_value = mock_query

    params = {
        "product": "Product1",
        "campaign_type": "Type1",
        "campaign": "Campaign1",
        "channel": "Channel1",
        "start_date": "2023-01-01",
        "end_date": "2023-01-02"
    }

    response = test_client.get("/marketing-data", params=params)

    assert response.status_code == 200
    assert response.json() == [
        {
            "product": "Product1",
            "campaign_type": "Type1",
            "campaign": "Campaign1",
            "channel": "Channel1",
            "date": "2023-01-01",
            "conversions": 664.1394510189357
        },
        {
            "product": "Product2",
            "campaign_type": "Type2",
            "campaign": "Campaign2",
            "channel": "Channel2",
            "date": "2023-01-02",
            "conversions": 82.07983229688519
        }
    ]
    mock_get_marketing_data_filter.assert_called_once_with(
        MarketingData, "Product1", "Type1", "Campaign1", "Channel1", "2023-01-01", "2023-01-02")
    mock_query.filter.assert_called_once_with("filter_expression")
