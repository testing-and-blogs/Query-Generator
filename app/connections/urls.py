from rest_framework.routers import SimpleRouter
from .views import ConnectionViewSet

router = SimpleRouter()
router.register(r'connections', ConnectionViewSet, basename='connection')

urlpatterns = router.urls
