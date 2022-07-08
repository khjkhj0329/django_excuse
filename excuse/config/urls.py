from django.contrib import admin
from django.urls import path, include
# from excuse.excuse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('excuse/', include('excuse.urls')),
    path('common/', include('common.urls')),
    path('calendar/', include('calendar.urls')),
    path('', include('excuse.urls')),
]