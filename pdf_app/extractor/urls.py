from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    path("", views.landing_view, name="landing"),

    path("app/", views.split_view, name="home"),

    path("login/", views_auth.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),
    path("register/", views_auth.register_view, name="register"),

    path("upload/", views.upload_and_extract),
    path("analyze/", views.analyze_selection),
    path("query/", views.query_table),
]

