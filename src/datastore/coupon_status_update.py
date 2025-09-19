from datetime import UTC, datetime

from mongoengine import DoesNotExist, ValidationError

from src.coupon.enums import CouponStatus
from src.dtos.coupon_status_update import CouponStatusUpdateDTO
from src.models.coupon import Coupon
from src.models.coupon_status_update import CouponStatusUpdate
from src.models.user import User


def create_status_update_for_coupon(
    coupon_id: str,
    status: CouponStatus,
    updated_by: str | None = None,
) -> CouponStatusUpdateDTO:
    user = None
    try:
        if updated_by:
            user = User.objects.get(id=updated_by)
    except (DoesNotExist, ValidationError) as e:
        raise ValueError(f"{updated_by} is not a valid user id") from e
    try:
        coupon = Coupon.objects.get(id=coupon_id)
    except (DoesNotExist, ValidationError) as e:
        raise ValueError(f"{coupon_id} is not a valid coupon id") from e

    update = CouponStatusUpdate(
        coupon=coupon,
        status=status,
        updatedBy=user,
        updatedOn=datetime.now(UTC),
    )
    update.save()
    return update.to_dto()


def get_latest_coupon_status_update(coupon_id: str) -> CouponStatusUpdateDTO:
    try:
        coupon = Coupon.objects.get(id=coupon_id)
    except (DoesNotExist, ValidationError) as e:
        raise ValueError(f"{coupon_id} is not a valid coupon id") from e
    latest: CouponStatusUpdate | None = (
        CouponStatusUpdate.objects(coupon=coupon).order_by("-updatedOn").first()
    )
    if not latest:
        raise ValueError(f"No status update found for coupon {coupon.id}")
    return latest.to_dto()
