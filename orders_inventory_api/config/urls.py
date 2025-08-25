"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ProductViewSet, CustomerViewSet, OrderViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView
from django.views.generic import RedirectView


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"orders", OrderViewSet, basename="order")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),

    # login/logout para SessionAuth
    path('api-auth/', RedirectView.as_view(url='/api-auth/login/', permanent=False)),
    path('api-auth/', include('rest_framework.urls')),

    # OpenAPI schema + UIs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
