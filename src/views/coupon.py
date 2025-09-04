import random
import string
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from mongoengine import DoesNotExist, ValidationError

from src.auth.middleware import UserClaims, get_current_user, require_admin
from src.coupon.enums import CouponStatus
from src.coupon.status import get_coupon_status, update_coupon_status
from src.datastore.coupon import batch_create_coupons, get_coupons, get_coupons_by_user
from src.datastore.coupon_template import get_or_none_template, get_template_by_id
from src.datastore.user import getUserByUserId
from src.dtos.user import UserDTO
from src.views.body.coupon import CouponList, CouponRequest, CouponResponse, StatusUpdateRequest

router = APIRouter(tags=["coupon"])


@router.get("/coupons/{target_user_id}")
def get_coupons_for_user(
    target_user_id: str, user: Annotated[UserClaims, Depends(get_current_user)]
) -> CouponList:
    target_user: UserDTO | None = None

    if len(target_user_id) == 24 and target_user_id.isalnum():
        try:
            target_user = getUserByUserId(target_user_id)
        except DoesNotExist as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {target_user_id} does not exist",
            ) from e
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{target_user_id} is not a valid mongo Object Id",
            ) from e
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{target_user_id} is not a valid mongo Object Id",
        )

    if target_user is None:
        raise RuntimeError(
            f"Could not get target User {target_user_id} requested by f{user.userId}"
        )

    if target_user.id != user.userId and not user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this user",
        )

    coupons = get_coupons_by_user(target_user_id)

    coupon_list: list[CouponResponse] = []
    total_price = 0
    total_unpaid_price = 0

    for coupon in coupons:
        template = get_template_by_id(coupon.template_id)
        coupon_status = get_coupon_status(coupon.id)
        coupon_list.append(
            CouponResponse(
                coupon_id=coupon.id,
                day=coupon.day,
                food_preference=template.food_preference,
                coupon_type=template.coupon_type,
                status=coupon_status,
                price=template.price,
                booked_on=coupon.booked_on,
            )
        )
        total_price += template.price
        if coupon_status == CouponStatus.COLLECTED:
            total_unpaid_price += template.price

    return CouponList(
        count=len(coupons),
        total_unpaid_price=total_unpaid_price,
        total_price=total_price,
        coupons=coupon_list,
    )


@router.post("/coupons/book", status_code=201)
def book_coupon(
    body: CouponRequest, user: Annotated[UserClaims, Depends(get_current_user)]
) -> None:
    if body.count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Count must be greater than zero",
        )

    template = get_or_none_template(
        couponType=body.coupon.coupon_type,
        foodPreference=body.coupon.food_preference,
    )
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching coupon template found",
        )

    alphabet = string.ascii_letters + string.digits
    batch_code = "".join(random.choices(alphabet, k=5))

    coupons = batch_create_coupons(
        day=body.coupon.day,
        template_id=template.id,
        booked_by=user.userId,
        batch_code=batch_code,
        batch_size=body.count,
    )

    for coupon in coupons:
        update_coupon_status(coupon_id=coupon.id, status=CouponStatus.BOOKED, updater_id=None)


@router.get("/coupons")
def get_all_coupons(
    _: Annotated[UserClaims, Depends(require_admin)],
) -> CouponList:
    coupons = get_coupons()

    coupon_list: list[CouponResponse] = []
    total_price = 0
    total_unpaid_price = 0

    for coupon in coupons:
        template = get_template_by_id(coupon.template_id)
        coupon_status = get_coupon_status(coupon.id)
        coupon_list.append(
            CouponResponse(
                coupon_id=coupon.id,
                day=coupon.day,
                food_preference=template.food_preference,
                coupon_type=template.coupon_type,
                status=coupon_status,
                price=template.price,
                booked_on=coupon.booked_on,
            )
        )
        total_price += template.price
        if coupon_status == CouponStatus.COLLECTED:
            total_unpaid_price += template.price

    return CouponList(
        count=len(coupons),
        total_unpaid_price=total_unpaid_price,
        total_price=total_price,
        coupons=coupon_list,
    )


@router.post("/coupons/status")
def make_status_update(
    body: StatusUpdateRequest,
    user: Annotated[UserClaims, Depends(get_current_user)],
    _: Annotated[UserClaims, Depends(require_admin)],
) -> None:
    try:
        update_coupon_status(body.coupon_id, status=body.status, updater_id=user.userId)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
