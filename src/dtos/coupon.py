from datetime import date

from pydantic import BaseModel


class CouponDTO(BaseModel):
    id: str
    day: date
    template_id: str
    booked_by: str
    booked_on: date
    batch_code: str
