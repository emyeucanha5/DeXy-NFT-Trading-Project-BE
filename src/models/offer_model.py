from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from utils.database import BaseModel
from sqlalchemy.orm import relationship, Mapped


class OfferModel(BaseModel):
    __tablename__ = "Offers"

    offer_id = Column(Integer, primary_key=True, nullable=False)
    offer_from_user_id = Column(
        Integer, ForeignKey("Users.user_id"), nullable=False
    )
    offer_price = Column(Float, nullable=False)
    offer_date = Column(Date, nullable=False)
    offer_item_id = Column(Integer, ForeignKey("Items.item_id"), nullable=False)
    offer_status = Column(String(20), nullable=False)

    user = relationship("UserModel", back_populates="offers")
    item = relationship("ItemModel", back_populates="offers")

    def __init__(
        self,
        offer_from_user_id: int,
        offer_price: float,
        offer_date: str,
        offer_item_id: int,
        offer_status: str,
    ):
        self.offer_from_user_id = offer_from_user_id
        self.offer_price = offer_price
        self.offer_date = offer_date
        self.offer_item_id = offer_item_id
        self.offer_status = offer_status
