from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

from mongoengine import DateField, Document, ReferenceField, StringField

from src.dtos.coupon import CouponDTO
from src.models.coupon_template import CouponTemplate
from src.models.user import User


class Coupon(Document):
    meta = {
        "indexes": [
            "day",
            "bookedBy",
            "batchCode",
            {"fields": ["day", "bookedBy"]},
        ]
    }
    day = DateField(required=True)
    template = ReferenceField(CouponTemplate, required=True)
    bookedBy = ReferenceField(User, required=True)
    bookedOn = DateField(default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")).date())
    batchCode = StringField()

    def to_dto(self) -> CouponDTO:
        return CouponDTO(
            id=self.id,
            day=self.day,
            template_id=str(self.template.id) if self.template else None,
            booked_by=str(self.bookedBy.id),
            booked_on=self.bookedOn,
            batch_code=self.batchCode,
        )

    @classmethod
    def from_dto(cls, dto: CouponDTO) -> Self:
        template = CouponTemplate.objects(id=dto.template_id).first()
        user = User.objects(id=dto.booked_by).first()
        return cls(
            day=dto.day,
            template=template,
            bookedBy=user,
            batchCode=dto.batch_code,
        )
