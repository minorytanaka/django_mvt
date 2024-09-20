from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("about/", include("about.urls", namespace="about")),
    path("", include("posts.urls", namespace="posts")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
