from pydantic import BaseModel, Field, validator
from web3 import Web3
from fastapi import HTTPException
from typing import Optional


class CreateUserRequestDto(BaseModel):
    user_wallet_address: str = Field(
        ...,
        example="0x1aBA989D0703cE6CC651B6109d02b39a9651aE5d",
        description="Wallet address of the user",
        type="string",
    )

    @validator("user_wallet_address")
    def validate_wallet_address(cls, value: str) -> str:
        if not Web3.is_address(value):
            raise HTTPException(
                status_code=422,
                detail=f"Failed! Wallet address {value} is not a valid Ethereum address.",
            )
        checksum_address = Web3.to_checksum_address(value)
        return checksum_address


class UpdateUserRequestDto(BaseModel):
    user_name: Optional[str] = Field(
        ...,
        example="John Doe",
        description="Name of the user",
        type="string",
    )
    user_email: Optional[str] = Field(
        ...,
        example="123@gmail.com",
        description="Email of the user",
        type="string",
    )
