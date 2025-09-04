from pydantic import BaseModel

from src.coupon.enums import CouponType, FoodPreference


class TemplateBody(BaseModel):
    food_preference: FoodPreference
    coupon_type: CouponType
    price: int


class PriceBody(BaseModel):
    food_preference: FoodPreference
    coupon_type: CouponType


class PriceResponse(BaseModel):
    price: int
