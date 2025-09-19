from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.middleware import UserClaims, require_admin
from src.coupon.enums import CouponStatus, CouponType
from src.coupon.status import get_coupon_status
from src.datastore.coupon import get_coupons
from src.datastore.coupon_template import get_template_by_id
from src.views.body.dashboard import DashboardResponse, DayStats, MealBreakdown, PaymentStats

router = APIRouter(tags=["dashboard"])


@router.get("/admin/dashboard")
def dashboard(_: Annotated[UserClaims, Depends(require_admin)]) -> DashboardResponse:
    coupons = get_coupons()

    total_coupons = len(coupons)
    unpaid_amount = 0
    unpaid_number = 0
    paid_amount = 0
    paid_number = 0
    uncollected_number = 0

    per_day = [
        DayStats(day=date(2025, mm, dd), meals=MealBreakdown(breakfast=0, lunch=0, dinner=0))
        for (mm, dd) in zip([9, 9, 9, 10, 10], [28, 29, 30, 1, 2], strict=False)
    ]

    for coupon in coupons:
        status = get_coupon_status(coupon.id)
        template = get_template_by_id(coupon.template_id)

        if status == CouponStatus.CANCELLED:
            total_coupons -= 1
            continue

        if status == CouponStatus.BOOKED:
            unpaid_amount += template.price
            unpaid_number += 1
        elif status == CouponStatus.PAID:
            uncollected_number += 1
            paid_number += 1
            paid_amount += template.price
        elif status == CouponStatus.COLLECTED:
            paid_number += 1
            paid_amount += template.price

        for day_stats in per_day:
            if day_stats.day == coupon.day:
                if template.coupon_type == CouponType.BREAKFAST:
                    day_stats.meals.breakfast += 1
                elif template.coupon_type == CouponType.LUNCH:
                    day_stats.meals.lunch += 1
                elif template.coupon_type == CouponType.DINNER:
                    day_stats.meals.dinner += 1

    response = DashboardResponse(
        total_coupons_booked=total_coupons,
        total_coupons_paid=paid_number,
        total_coupons_collected=paid_number - uncollected_number,
        total_coupons_unpaid=unpaid_number,
        per_day_stats=per_day,
        payment_stats=PaymentStats(paid_amount=paid_amount, unpaid_amount=unpaid_amount),
    )

    return response
