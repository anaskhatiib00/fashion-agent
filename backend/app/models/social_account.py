from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    page_id = Column(String, nullable=False)
    page_name = Column(String, nullable=False)
    page_access_token = Column(Text, nullable=False)