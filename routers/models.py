from pydantic import BaseModel
from datetime import date


class MarketingDataResponse(BaseModel):
    product: str
    campaign_type: str
    campaign: str
    channel: str
    date: date
    conversions: float


class MarketingDataPieChartResponse(BaseModel):
    channel: str
    net_sales: float
    percentage: float


class MarketingDataStackedAreaChartResponse(BaseModel):
    date: date
    channel: str
    net_sales: float
