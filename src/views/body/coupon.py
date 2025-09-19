from datetime import date

from pydantic import BaseModel

from src.coupon.enums import CouponStatus, CouponType, FoodPreference


class CouponBody(BaseModel):
    day: date
    food_preference: FoodPreference
    coupon_type: CouponType


class CouponRequest(BaseModel):
    count: int
    coupon: CouponBody


class StatusUpdateRequest(BaseModel):
    coupon_id: str
    status: CouponStatus


class CouponResponse(BaseModel):
    coupon_id: str
    day: date
    food_preference: FoodPreference
    coupon_type: CouponType
    status: CouponStatus
    price: int
    booked_on: date
    booked_by: str


class CouponList(BaseModel):
    count: int
    total_unpaid_price: int
    total_price: int
    coupons: list[CouponResponse]


class CouponStatusUpdateBody(BaseModel):
    coupon_id: str
    new_status: CouponStatus
