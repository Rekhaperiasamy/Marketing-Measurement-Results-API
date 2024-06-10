# routers/marketing.py
from fastapi import APIRouter, Query, HTTPException

from sqlalchemy.sql import func
from pydantic import TypeAdapter
from typing import List, Optional
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
import logging

from database.database import Database
from database.filters import Filters
from database.models import MarketingData
from routers.models import MarketingDataResponse, MarketingDataPieChartResponse, MarketingDataStackedAreaChartResponse

router = APIRouter()

db_session = Database().get_session()


@router.get("/marketing-data", response_model=list[MarketingDataResponse])
def read_marketing_data(
    product: Optional[str] = Query(None, description="Filter by product"),
    campaign_type: Optional[str] = Query(
        None, description="Filter by campaign type"),
    campaign: Optional[str] = Query(None, description="Filter by campaign"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    start_date: Optional[date] = Query(
        None, description="Start date in the format yyyy-mm-dd"),
    end_date: Optional[date] = Query(
        None, description="End date in the format yyyy-mm-dd"),
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset for pagination")
):

    try:
        filters = Filters.get_marketing_data_filter(
            MarketingData,
            product,
            campaign_type,
            campaign,
            channel,
            start_date,
            end_date
        )
        marketing_data = db_session.query(MarketingData).filter(
            *filters).limit(limit).offset(offset).all()

        adapter = TypeAdapter(List[MarketingDataResponse])
        return adapter.validate_python(marketing_data)

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@ router.get("/pie-chart", response_model=list[MarketingDataPieChartResponse])
def show_pie_chart(
    product: Optional[str] = Query(None, description="Filter by product"),
    campaign_type: Optional[str] = Query(
        None, description="Filter by campaign type"),
    campaign: Optional[str] = Query(None, description="Filter by campaign"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    start_date: Optional[date] = Query(
        None, description="Start date in the format yyyy-mm-dd"),
    end_date: Optional[date] = Query(
        None, description="End date in the format yyyy-mm-dd")
):
    try:
        filters = Filters.get_marketing_data_filter(
            MarketingData,
            product,
            campaign_type,
            campaign,
            channel,
            start_date,
            end_date
        )
        pie_chart_data = db_session.query(
            MarketingData.channel,
            func.sum(MarketingData.conversions)
        ).filter(*filters).group_by(MarketingData.channel).all()

        total_value = sum(value for _, value in pie_chart_data)
        pie_chart = [{'channel': key, 'net_sales': value, 'percentage': (
            value / total_value) * 100} for key, value in pie_chart_data]

        adapter = TypeAdapter(List[MarketingDataPieChartResponse])
        return adapter.validate_python(pie_chart)

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@ router.get("/stacked-area-chart", response_model=list[MarketingDataStackedAreaChartResponse])
def show_stacked_area_chart(
    product: Optional[str] = Query(None, description="Filter by product"),
    campaign_type: Optional[str] = Query(
        None, description="Filter by campaign type"),
    campaign: Optional[str] = Query(None, description="Filter by campaign"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    start_date: Optional[date] = Query(
        None, description="Start date in the format yyyy-mm-dd"),
    end_date: Optional[date] = Query(
        None, description="End date in the format yyyy-mm-dd")
):

    try:
        filters = Filters.get_marketing_data_filter(
            MarketingData,
            product,
            campaign_type,
            campaign,
            channel,
            start_date,
            end_date
        )
        stacked_area_chart_data = db_session.query(
            MarketingData.channel,
            MarketingData.date,
            func.sum(MarketingData.conversions)
        ).filter(*filters).group_by(MarketingData.channel, MarketingData.date).order_by(MarketingData.date).all()

        stacked_area_chart = [{'channel': channel, 'date': date,
                               'net_sales': net_sales} for channel, date, net_sales in stacked_area_chart_data]

        adapter = TypeAdapter(List[MarketingDataStackedAreaChartResponse])
        return adapter.validate_python(stacked_area_chart)

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
