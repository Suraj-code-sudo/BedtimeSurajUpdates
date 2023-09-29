from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from books.views import CombinedNarration

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', views.BookViewSet,basename="books")
router.register(r'narrations', views.RecordingViewSet, basename="narrations")
router.register(r'recording_requests', views.RecordingRequestViewSet, basename="recording_requests")
router.register(r'recording_url', views.UrlViewSet, basename="recording_url")

# router.register(r'recordings', views.RecordingViewSet, basename="recordings")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(
        'recordings/', views.RecordingViewSet.as_view(
            {
                "get": "list",
                'post': 'create'
            }
        ),
        name='recordings'
    ),
    path('combined-narrations/',CombinedNarration.as_view({'post': 'create'}), name='combined-narrations'),

]