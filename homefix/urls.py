from django.contrib import admin
from django.urls import include, path
from services import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("book/", views.book_service, name="book_service"),
    path("service/", include("services.urls")),
]
