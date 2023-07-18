from drf_yasg import openapi

email_field = openapi.Schema(
    "email",
    type=openapi.TYPE_STRING,
    description="Email Field",
)

password_field = openapi.Schema(
    "password",
    type=openapi.TYPE_STRING,
    description="Password Field",
)

first_name_field = openapi.Schema(
    "first_name",
    type=openapi.TYPE_STRING,
    description="First Name Field",
)

last_name_field = openapi.Schema(
    "last_name",
    type=openapi.TYPE_STRING,
    description="Last Name Field",
)

username_field = openapi.Schema(
    "username", type=openapi.TYPE_STRING, description="Username"
)

register_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="Register Data",
    properties={
        "email": email_field,
        "password": password_field,
        "username": username_field,
        "first_name": first_name_field,
        "last_name": last_name_field,
    },
    required=["email", "password", "username"],
)

login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="Login Data",
    properties={
        "email": email_field,
        "password": password_field,
    },
    required=["email", "password"],
)
