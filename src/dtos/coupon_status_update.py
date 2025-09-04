from datetime import datetime

from pydantic import BaseModel

from src.coupon.enums import CouponStatus


class CouponStatusUpdateDTO(BaseModel):
    couponId: str
    updatedOn: datetime
    status: CouponStatus
    updatedBy: str | None = None
