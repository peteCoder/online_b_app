
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    # path('api/', include('api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error Pages -- ATTEND TO THIS LATER

# def not_found(request, exception):
#     return render(request, 'not_found.html', {})

# handler404 = 'travel_project.urls.not_found'
