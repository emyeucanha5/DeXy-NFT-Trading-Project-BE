from typing import List
from models.item_model import ItemModel
from models.shopping_cart_item_model import ShoppingCartItemModel
from sqlalchemy.orm import Session
from models.user_model import UserModel

from schemas.shopping_cart_item.request_dto import (
    CreateShoppingCartItemRequestDto,
)


class ShoppingCartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_shopping_cart_items_by_user_wallet(
        self, user_wallet_address: str
    ) -> List[ShoppingCartItemModel]:
        return (
            self.db.query(ShoppingCartItemModel)
            .join(
                UserModel,
                UserModel.user_id
                == ShoppingCartItemModel.shopping_cart_item_user_id,
            )
            .filter(UserModel.user_wallet_address == user_wallet_address)
            .all()
        )

    def add_shopping_cart_item(
        self, payload: CreateShoppingCartItemRequestDto, user: dict
    ) -> None:
        new_shopping_cart_item = ShoppingCartItemModel(
            shopping_cart_item_user_id=user["user_id"],
            shopping_cart_item_item_id=payload.item_id,
        )

        self.db.add(new_shopping_cart_item)
        self.db.commit()

    def delete_shopping_cart_item(self, shopping_cart_item_id: int) -> None:
        self.db.query(ShoppingCartItemModel).filter(
            ShoppingCartItemModel.shopping_cart_item_id == shopping_cart_item_id
        ).delete()
        self.db.commit()

    def get_shopping_cart_item_by_user_id_and_item_id(
        self, user_id: int, item_id: int
    ) -> ShoppingCartItemModel:
        return (
            self.db.query(ShoppingCartItemModel)
            .filter(
                ShoppingCartItemModel.shopping_cart_item_user_id == user_id,
                ShoppingCartItemModel.shopping_cart_item_item_id == item_id,
            )
            .first()
        )

    def get_items_in_cart_by_user_wallet(
        self, user_wallet_address: str
    ) -> List[ItemModel]:
        return (
            self.db.query(
                ShoppingCartItemModel.shopping_cart_item_id,
                ItemModel.item_name.label("item_name"),
                ItemModel.item_price.label("item_price"),
                ItemModel.item_price_currency.label("item_price_currency"),
                UserModel.user_wallet_address.label("user_wallet_address"),
                ItemModel.item_image.label("item_image"),
            )
            .join(
                UserModel,
                UserModel.user_id
                == ShoppingCartItemModel.shopping_cart_item_user_id,
            )
            .join(
                ItemModel,
                ItemModel.item_id
                == ShoppingCartItemModel.shopping_cart_item_item_id,
            )
            .filter(UserModel.user_wallet_address == user_wallet_address)
            .all()
        )