"""API URL configuration for NetBox Custom Widget plugin."""

from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.register("endpoints", views.CustomAPIEndpointViewSet)

urlpatterns = router.urls
