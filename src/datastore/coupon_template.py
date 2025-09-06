from src.coupon.enums import CouponType, FoodPreference
from src.dtos.coupon_template import CouponTemplateDTO
from src.models.coupon_template import CouponTemplate
from src.models.user import User


def create_template(dto: CouponTemplateDTO) -> None:
    created_by = User.objects(id=dto.created_by).first() if dto.created_by else None
    template = CouponTemplate(
        couponType=dto.coupon_type,
        foodPreference=dto.food_preference,
        price=dto.price,
        createdBy=created_by,
    )
    template.save()


def get_or_none_template(
    foodPreference: FoodPreference, couponType: CouponType
) -> CouponTemplateDTO | None:
    template = CouponTemplate.objects(
        foodPreference=foodPreference,
        couponType=couponType,
    ).first()
    return template.to_dto() if template else None


def get_template_by_id(template_id: str) -> CouponTemplateDTO:
    template: CouponTemplate = CouponTemplate.objects.get(id=template_id)
    return template.to_dto()


def edit_template_price(
    foodPreference: FoodPreference, couponType: CouponType, newPrice: int
) -> None:
    CouponTemplate.objects(
        foodPreference=foodPreference,
        couponType=couponType,
    ).update_one(set__price=newPrice)


def delete_template(foodPreference: FoodPreference, couponType: CouponType) -> None:
    CouponTemplate.objects(
        foodPreference=foodPreference,
        couponType=couponType,
    ).delete()
