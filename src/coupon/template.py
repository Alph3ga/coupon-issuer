from src.coupon.enums import CouponType, FoodPreference
from src.datastore.coupon_template import (
    create_template,
    edit_template_price,
    get_or_none_template,
)
from src.dtos.coupon_template import CouponTemplateDTO


def upsert_template(
    foodPreference: FoodPreference, couponType: CouponType, price: int, user_id: str
) -> None:
    if price < 0:
        raise ValueError(f"Price cannot be less than zero, was {price}")

    existing = get_or_none_template(foodPreference, couponType)
    if existing:
        edit_template_price(foodPreference, couponType, price)
        return

    dto = CouponTemplateDTO(
        id="placeholder",
        coupon_type=couponType,
        food_preference=foodPreference,
        price=price,
        created_by=user_id,
    )

    create_template(dto)


def does_template_exist(foodPreference: FoodPreference, couponType: CouponType) -> bool:
    return bool(get_or_none_template(foodPreference, couponType))


def get_price(foodPreference: FoodPreference, couponType: CouponType) -> int:
    template = get_or_none_template(foodPreference, couponType)
    if not template:
        raise ValueError(f"Template does not exist for {couponType} {foodPreference}")
    return template.price
