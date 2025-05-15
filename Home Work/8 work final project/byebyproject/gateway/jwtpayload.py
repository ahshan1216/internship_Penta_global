import jwt
import datetime
from django.conf import settings
from .models import AssignRole


def get_user_role(user):
    role_qs = AssignRole.objects.filter(user=user).select_related('role')
    return role_qs.first().role.name if role_qs.exists() else None


def create_jwt_token(user):
    role = get_user_role(user)
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token
