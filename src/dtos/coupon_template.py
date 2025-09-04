from pydantic import BaseModel


class CouponTemplateDTO(BaseModel):
    id: str
    coupon_type: str
    food_preference: str
    price: int
    created_by: str | None
