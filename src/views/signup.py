from fastapi import APIRouter, HTTPException, status

from src.auth.utils import create_jwt
from src.crypto_utils import checkPassword, encyptPassword
from src.datastore.user import create_user, get_or_none_user_by_flat_number, getUserIdByFlatNumber
from src.dtos.user import UserDTO
from src.user.registration import clean_flat_number, validate_user_info
from src.views.body.signup import LoginBody, SignupBody, TokenResponse

router = APIRouter(tags=["signup"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(body: SignupBody) -> TokenResponse:
    try:
        cleanedFlatNumber = clean_flat_number(body.flat_number)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    existing = get_or_none_user_by_flat_number(cleanedFlatNumber)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists, log in instead."
        )

    valid, reason = validate_user_info(
        email=body.email, password=body.password, flat_number=cleanedFlatNumber
    )
    if not valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    hashedPass = encyptPassword(body.password) if body.password else None
    userDTO = UserDTO(
        id="placeholder",
        flatNumber=cleanedFlatNumber,
        email=body.email,
        hashedPass=hashedPass,
        isAdmin=False,
    )
    user_id = create_user(userDTO)

    token = create_jwt(flat_number=cleanedFlatNumber, is_admin=False, user_id=user_id)

    return TokenResponse(
        token_type="bearer",
        access_token=token,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginBody) -> TokenResponse:
    cleanedFlatNumber = clean_flat_number(body.flat_number)
    existing = get_or_none_user_by_flat_number(cleanedFlatNumber)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist, sign up instead."
        )
    user_id = getUserIdByFlatNumber(cleanedFlatNumber)
    token = create_jwt(flat_number=existing.flatNumber, is_admin=existing.isAdmin, user_id=user_id)
    response = TokenResponse(
        token_type="bearer",
        access_token=token,
    )

    if existing.hashedPass is None:
        return response

    if body.password and checkPassword(body.password, existing.hashedPass):
        return response

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Recheck flat number or password"
    )
