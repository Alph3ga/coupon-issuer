from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.middleware import UserClaims, get_current_user, require_admin
from src.coupon.template import upsert_template
from src.datastore.coupon_template import get_all_templates, get_or_none_template
from src.views.body.template import PriceBody, PriceResponse, TemplateBody

router = APIRouter(tags=["template"])


@router.post("/template/edit", status_code=201)
def edit_template(
    body: TemplateBody,
    user: Annotated[UserClaims, Depends(get_current_user)],
    _: Annotated[UserClaims, Depends(require_admin)],
) -> None:
    upsert_template(body.food_preference, body.coupon_type, body.price, user.userId)


@router.get("/template/price")
def get_template_price(body: PriceBody) -> PriceResponse:
    template = get_or_none_template(body.food_preference, body.coupon_type)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The template for {body.food_preference} {body.coupon_type} does not exist",
        )
    return PriceResponse(price=template.price)


@router.get("/template")
def get_templates() -> list[TemplateBody]:
    templates = get_all_templates()

    return [
        TemplateBody(food_preference=t.food_preference, coupon_type=t.coupon_type, price=t.price)
        for t in templates
    ]
