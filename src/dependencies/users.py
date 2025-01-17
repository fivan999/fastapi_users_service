from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.dependencies.tokens import JWTTokenDep
from src.utils.enums import TokenEnum, TokenTypeEnum
from src.utils.tokens import get_validated_token_data


async def get_current_user_id_by_access_token(token: JWTTokenDep) -> int:
    """
    Getting user's id from jwt token

    Args:
        token (JWTTokenDep): jwt token

    Raises:
        HTTPException: user's token is not valid

    Returns:
        int: user's id
    """
    token_status, payload = get_validated_token_data(
        token, TokenTypeEnum.ACCESS
    )
    if token_status != TokenEnum.TOKEN_IS_VALID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=token_status.value
        )
    return int(payload.get("sub"))


UserIdDep = Annotated[int, Depends(get_current_user_id_by_access_token)]
