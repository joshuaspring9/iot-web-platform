from django.urls import include, path
from rest_framework import routers
import oauth2_provider.views as oauth2_views
from django.conf import settings
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'devices', views.SmartHomeDeviceViewSet)
router.register(r'datafiles', views.DataFileViewSet, basename='datafiles')


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<int:pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<int:pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<int:pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<int:pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='django_rest_framework')),
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),
]