from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    #incluir las urls condiguradas en pos.urls
    path("pos/",include('pos.urls', namespace="pos")),
]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)