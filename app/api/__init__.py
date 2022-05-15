from fastapi import APIRouter

from app.api.auth.auth_register import auth_register
from app.api.auth.auth_login import auth_login, LoginResponseModel
from app.api.auth.auth_logout import auth_logout
from app.api.auth.auth_refresh_token import auth_refresh_token, RefreshTokenResponseModel
from app.api.auth.get_profile import get_profile, GetProfileResponseModel


api_router = APIRouter()

api_router.add_api_route('/api/v1/auth/register', auth_register,
                         methods=['POST'], tags=['Auth'], status_code=201)
api_router.add_api_route('/api/v1/auth/login', auth_login,
                         methods=['POST'], tags=['Auth'], response_model=LoginResponseModel)
api_router.add_api_route('/api/v1/auth/logout', auth_logout,
                         methods=['POST'], tags=['Auth'], status_code=204)
api_router.add_api_route('/api/v1/auth/refresh-token', auth_refresh_token,
                         methods=['POST'], tags=['Auth'], response_model=RefreshTokenResponseModel)
api_router.add_api_route('/api/v1/auth/profile', get_profile,
                         methods=['GET'], tags=['Auth'], response_model=GetProfileResponseModel)
