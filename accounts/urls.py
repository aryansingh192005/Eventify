from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "register/",
        views.register_view,
        name="register",
    ),
    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),
    path(
        "profile/edit/",
        views.edit_profile_view,
        name="edit_profile",
    ),
    path(
    "admin/users/",
    views.admin_user_list,
    name="admin_user_list",
),

path(
    "admin/users/<int:user_id>/",
    views.admin_user_detail,
    name="admin_user_detail",
),

path(
    "admin/users/<int:user_id>/toggle-status/",
    views.admin_user_toggle_status,
    name="admin_user_toggle_status",
),

path(
    "admin/users/<int:user_id>/delete/",
    views.admin_user_delete,
    name="admin_user_delete",
),
]