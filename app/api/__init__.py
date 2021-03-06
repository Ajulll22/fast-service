from fastapi import APIRouter

from app.api.auth.auth_register import auth_register
from app.api.auth.auth_login import auth_login, LoginResponseModel
from app.api.auth.auth_logout import auth_logout
from app.api.auth.auth_refresh_token import auth_refresh_token, RefreshTokenResponseModel
from app.api.auth.get_profile import get_profile, GetProfileResponseModel
from app.api.auth.edit_profile import edit_profile

from app.api.transaction.create_transaction import create_transaction, CreateTransactionResponseModel
from app.api.transaction.create_transaction_item import create_transaction_item, CreateTransactionItemResponseModel
from app.api.transaction.get_transaction_detail import get_transaction_detail, GetTransactionDetailResponseModel


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
api_router.add_api_route('/api/v1/auth/profile', edit_profile,
                         methods=['PUT'], tags=['Auth'], status_code=204)


api_router.add_api_route('/api/v1/transaction', create_transaction,
                         methods=['POST'], tags=['Transaction'], response_model=CreateTransactionResponseModel)
api_router.add_api_route('/api/v1/transaction-item', create_transaction_item,
                         methods=['POST'], tags=['Transaction'], response_model=CreateTransactionItemResponseModel)
api_router.add_api_route('/api/v1/transaction/{transaction_id}', get_transaction_detail,
                         methods=['GET'], tags=['Transaction'], response_model=GetTransactionDetailResponseModel)
