from datetime import UTC, datetime

from mongoengine import DoesNotExist, ValidationError

from src.coupon.enums import CouponStatus
from src.datastore.coupon import get_coupon_by_id
from src.dtos.coupon_status_update import CouponStatusUpdateDTO
from src.models.coupon import Coupon
from src.models.coupon_status_update import CouponStatusUpdate
from src.models.user import User


def create_status_update_for_coupon(
    coupon_id: str,
    status: CouponStatus,
    updated_by: User | None = None,
) -> CouponStatusUpdateDTO:
    try:
        coupon = get_coupon_by_id(coupon_id)
    except (DoesNotExist, ValidationError) as e:
        raise ValueError(f"{coupon_id} is not a valid coupon id") from e

    update = CouponStatusUpdate(
        coupon=coupon,
        status=status,
        updatedBy=updated_by,
        updatedOn=datetime.now(UTC),
    )
    update.save()
    return update.to_dto()


def get_latest_coupon_status_update(coupon: Coupon) -> CouponStatusUpdateDTO:
    latest = CouponStatusUpdate.objects(coupon=coupon).order_by("-updatedOn").first()
    if not latest:
        raise ValueError(f"No status update found for coupon {coupon.id}")
    return latest.to_dto()
