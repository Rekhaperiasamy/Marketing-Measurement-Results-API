from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarketingData(Base):
    __tablename__ = 'marketing_data'

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    campaign_type = Column(String)
    campaign = Column(String)
    channel = Column(String)
    date = Column(Date)
    conversions = Column(Numeric)
