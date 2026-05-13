from src.security.token_service import load_token, decode_token
import functools

PERMISSIONS_BY_ROLE = {
    "sales": [
        "create_event",
        "delete_event",
        "update_event",
        "filter_event",
        "update_contract",
        "sort_contract",
        "filter_contract",
        "create_customer",
        "update_customer",
        "delete_customer",
    ],
    "management": [
        "create_contract",
        "delete_contract",
        "sort_contract",
        "filter_contract",
        "update_contract",
        "assign_support_staff",
        "filter_event",
        "update_event",
        "filter_event_by_contact",
        "create_employee",
        "update_employee",
        "delete_employee",
        "create_customer",
        "update_customer",
        "delete_customer",
    ],
    "support": ["filter_event", "update_event"],
}


class Unauthenticated(Exception):
    pass


class Unauthorized(Exception):
    pass


def get_current_user_role():
    token = load_token()
    if not token:
        print("Not token")
    payload = decode_token(token)
    return payload.get("role")


def has_permissions(permission: str) -> bool:
    role = get_current_user_role()
    if not role:
        return False
    return permission in PERMISSIONS_BY_ROLE.get(role, [])


def require_permission(permission: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_permissions(permission):
                print(f"Access denied. Premission required: {permission}")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator
