from datetime import date

from src.dtos.coupon import CouponDTO
from src.models.coupon import Coupon
from src.models.coupon_template import CouponTemplate
from src.models.user import User


def create_coupon(
    day: date,
    template_id: str | None,
    booked_by: str,
    batch_code: str,
) -> None:
    template = CouponTemplate.objects(id=template_id).first() if template_id else None
    user = User.objects(id=booked_by).first()

    coupon = Coupon(
        day=day,
        template=template,
        bookedBy=user,
        batchCode=batch_code,
    )
    coupon.save()


def batch_create_coupons(
    day: date, template_id: str | None, booked_by: str, batch_code: str, batch_size: int
) -> list[CouponDTO]:
    template = CouponTemplate.objects(id=template_id).first() if template_id else None
    user = User.objects(id=booked_by).first()

    coupons = [
        Coupon(
            day=day,
            template=template,
            bookedBy=user,
            batchCode=batch_code,
        )
        for _ in range(batch_size)
    ]

    Coupon.objects.insert(coupons, load_bulk=False)

    return [c.to_dto() for c in coupons]


def get_coupons_by_batch(batch_code: str) -> list[CouponDTO]:
    coupons: list[Coupon] = Coupon.objects.filter(batchCode=batch_code).all()
    return [c.to_dto() for c in coupons]


def get_coupons_by_user(user_id: str) -> list[CouponDTO]:
    coupons = Coupon.objects.filter(bookedBy=user_id)
    return [c.to_dto() for c in coupons]


def get_coupon_by_id(id: str) -> CouponDTO:
    coupon: Coupon = Coupon.objects().get(id=id)
    return coupon.to_dto()


def get_coupons_by_day(day: date) -> list[CouponDTO]:
    coupons = Coupon.objects(day=day)
    return [c.to_dto() for c in coupons]


def get_coupons() -> list[CouponDTO]:
    coupons = Coupon.objects.all()
    return [c.to_dto() for c in coupons]
