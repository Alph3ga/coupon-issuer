from enum import StrEnum, auto


class FoodPreference(StrEnum):
    VEGETARIAN = auto()
    NON_VEGETARIAN = auto()


class CouponType(StrEnum):
    BREAKFAST = auto()
    LUNCH = auto()
    DINNER = auto()


class CouponStatus(StrEnum):
    BOOKED = auto()
    PAID = auto()
    COLLECTED = auto()
    CANCELLED = auto()
