from src.coupon.enums import CouponStatus
from src.datastore.coupon_status_update import (
    create_status_update_for_coupon,
    get_latest_coupon_status_update,
)


def update_coupon_status(coupon_id: str, status: CouponStatus, updater_id: str | None) -> None:
    create_status_update_for_coupon(coupon_id=coupon_id, status=status, updated_by=updater_id)


def get_coupon_status(coupon_id: str) -> CouponStatus:
    status_update = get_latest_coupon_status_update(coupon_id)
    return status_update.status
