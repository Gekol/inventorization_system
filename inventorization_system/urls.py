"""inventorization_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework_nested import routers

from auth_service import views as auth_service_views
from inventorization_service import views as inventory_service_views
from rms_service import views as cms_service_views
from analytics_service import views as analytics_service_views

router = routers.DefaultRouter()
router.register('users', auth_service_views.UserViewSet, basename="users")
router.register('inventory_service', analytics_service_views.ItemTypesViewSet, basename="inventory_service")
router.register('repair_service', analytics_service_views.ItemTypesViewSet, basename="repair_service")
router.register('analytics_service', analytics_service_views.AnalyticsViewSet, basename="analytics_service")

inventory_service_router = routers.NestedDefaultRouter(router, 'inventory_service')
inventory_service_router.register('items', inventory_service_views.ItemViewSet, basename="fixed_items")
repair_service_router = routers.NestedDefaultRouter(router, 'repair_service')
repair_service_router.register('items', cms_service_views.RepairViewSet, basename="broken_items")

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  path('', include(inventory_service_router.urls)),
                  path('', include(repair_service_router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
              ] + staticfiles_urlpatterns()
