from django.urls import path, include
from rest_framework import routers
from .views import index, ProductoView
from django.contrib import admin

router = routers.DefaultRouter()
router.register('productos', ProductoView, 'producto')

urlpatterns = [
    path('', index, name="cliente_index"),
    path('api/v1/', include(router.urls)),
    # path("admin/", admin.site.urls),
]
