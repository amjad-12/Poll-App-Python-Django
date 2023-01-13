from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('poll', views.PollViewSet, basename='poll')
router.register('vote', views.VoteViewSet, basename='vote')
router.register('customers', views.CustomersViewSet, basename='customers')

# nested route: poll/<pk>/choices/<pk>
poll_router = routers.NestedDefaultRouter(
    router, 'poll', lookup='poll')
poll_router.register('choices', views.ChoiceViewSet,
                         basename='choices')

urlpatterns = router.urls + poll_router.urls