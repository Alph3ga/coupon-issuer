from datetime import date

from pydantic import BaseModel


class MealBreakdown(BaseModel):
    breakfast: int
    lunch: int
    dinner: int


class DayStats(BaseModel):
    day: date
    meals: MealBreakdown


class PaymentStats(BaseModel):
    paid_amount: float
    unpaid_amount: float


class DashboardResponse(BaseModel):
    total_coupons_booked: int
    total_coupons_paid: int
    total_coupons_collected: int
    total_coupons_unpaid: int
    per_day_stats: list[DayStats]
    payment_stats: PaymentStats
