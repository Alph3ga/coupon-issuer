from typing import Self

from mongoengine import DateTimeField, Document, EnumField, ReferenceField

from src.coupon.enums import CouponStatus
from src.dtos.coupon_status_update import CouponStatusUpdateDTO
from src.models.coupon import Coupon
from src.models.user import User


class CouponStatusUpdate(Document):
    meta = {"indexes": [{"fields": ["coupon", "-updatedOn"]}]}
    coupon = ReferenceField(Coupon, required=True)
    updatedOn = DateTimeField(unique=True, required=True)
    status = EnumField(CouponStatus, use_value=True, required=True)
    updatedBy = ReferenceField(User)

    def to_dto(self) -> CouponStatusUpdateDTO:
        return CouponStatusUpdateDTO(
            id=str(self.id),
            couponId=str(self.coupon.id),
            updatedOn=self.updatedOn,
            status=self.status,
            updatedBy=str(self.updatedBy.id) if self.updatedBy else None,
        )

    @classmethod
    def from_dto(cls, dto: CouponStatusUpdateDTO) -> Self:
        coupon = Coupon.objects.get(id=dto.couponId)
        updated_by = User.objects.get(id=dto.updatedBy) if dto.updatedBy else None
        return cls(
            coupon=coupon,
            updatedOn=dto.updatedOn,
            status=dto.status,
            updatedBy=updated_by,
        )
