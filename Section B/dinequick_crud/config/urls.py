from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="menu-list", permanent=False), name="home"),
    path("panel/", admin.site.urls),
    re_path(r"^admin/(?P<path>.*)$", RedirectView.as_view(url="/panel/%(path)s", permanent=False)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("menuapp.urls")),
]


