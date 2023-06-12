from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from envs import JWT_SECRET

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)



# {
#   "email": "kek@mail.ru",
#   "password": "5795798",
#   "is_active": true,
#   "is_superuser": false,
#   "is_verified": false,
#   "username": "kek"
# }