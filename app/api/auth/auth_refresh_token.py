from pydantic import BaseModel
import sqlalchemy as sa
from fastapi.exceptions import HTTPException
from fastapi import Depends

from app.models.user import User
from app.models.user_login import UserLogin
from app.api_models.base_response import BaseResponseModel
from app.utils.generate_access_token import generate_access_token
from app.dependencies.get_db_session import get_db_session
from app.config import config


class RefreshTokenData(BaseModel):
    refresh_token: str


class RefreshTokenDataResponseModel(BaseModel):
    access_token: str
    expired_at: int


class RefreshTokenResponseModel(BaseResponseModel):
    data: RefreshTokenDataResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'refresh_token': 'abc.def.ghi',
                    'expired_at': 1234
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def auth_refresh_token(data: RefreshTokenData, session=Depends(get_db_session)):
    # check refresh token
    user_login = session.execute(
        sa.select(
            UserLogin.id,
            User.id.label('user_id'),
            User.username
        ).where(
            UserLogin.user_id == User.id,
            UserLogin.refresh_token == data.refresh_token
        )
    ).fetchone()

    if not user_login:
        raise HTTPException(400, detail='Refresh token not found')

    # extend exp refresh token
    session.execute(
        sa.update(
            UserLogin
        ).values(
            expired_at=sa.func.TIMESTAMPADD(
                sa.text('SECOND'),
                config.REFRESH_TOKEN_EXPIRATION,
                sa.func.NOW()
            )
        )
    )

    # generate new access token
    payload = {
        'uid': user_login.user_id,
        'username': user_login.username
    }

    access_token, expired_at = generate_access_token(payload)

    session.commit()

    return RefreshTokenResponseModel(
        data=RefreshTokenDataResponseModel(
            access_token=access_token,
            expired_at=expired_at
        )
    )
