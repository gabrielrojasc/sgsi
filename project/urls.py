"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from base.views import debug as debug_views
from base.views import misc as misc_views

debug_patterns = [
    path("request/", debug_views.HttpRequestPrintView.as_view(), name="debug-request"),
]

urlpatterns = [
    path("admin/", include("loginas.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("debug/", include(debug_patterns)),
    path("regions/", include("regions.urls")),
    path("", include("dummy_app.urls")),
    path("", misc_views.index, name="home"),
]

if settings.DEBUG:
    if not settings.TEST:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.ENABLE_DEBUG_TOOLBAR:
        # others libraries
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


# custom error views
handler400 = "base.views.misc.bad_request_view"
handler403 = "base.views.misc.permission_denied_view"
handler404 = "base.views.misc.page_not_found_view"
handler500 = "base.views.misc.server_error_view"
