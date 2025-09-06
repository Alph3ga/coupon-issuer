from datetime import UTC, datetime
from typing import Self

from mongoengine import DateTimeField, Document, EnumField, IntField, ReferenceField

from src.coupon.enums import CouponType, FoodPreference
from src.dtos.coupon_template import CouponTemplateDTO
from src.models.user import User


class CouponTemplate(Document):
    couponType = EnumField(CouponType, use_value=True)
    foodPreference = EnumField(FoodPreference, use_value=True)
    price = IntField(min_value=0)
    createdOn = DateTimeField(default=lambda: datetime.now(tz=UTC))
    createdBy = ReferenceField(User)

    def to_dto(self) -> CouponTemplateDTO:
        return CouponTemplateDTO(
            id=str(self.id),
            coupon_type=self.couponType,
            food_preference=self.foodPreference,
            price=self.price,
            created_by=str(self.createdBy.id) if self.createdBy else None,
        )

    @classmethod
    def from_dto(cls, dto: CouponTemplateDTO) -> Self:
        user = None
        if dto.created_by:
            from src.models.user import User

            user = User.objects(id=dto.created_by).first()

        return cls(
            couponType=dto.coupon_type,
            foodPreference=dto.food_preference,
            price=dto.price,
            createdBy=user,
        )
