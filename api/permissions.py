from rest_framework.permissions import (
   BasePermission, IsAdminUser, DjangoModelPermissions
)
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope


class IsAdminOrHasModelPermissionsOrTokenHasScope(BasePermission):
    """
    The user is authenticated using some backend or the token has the right scope
    This only returns True if the user is authenticated, but not using a token
    or using a token, and the token has the correct scope.
    This is usefull when combined with the DjangoModelPermissions to allow people browse
    the browsable api's if they log in using the a non token based middleware,
    and let them access the api's using a rest client with a token
    """
    def has_permission(self, request, view):
        is_authenticated = IsAdminUser().has_permission(request, view) or DjangoModelPermissions().has_permission(request, view)
        oauth2authenticated = False
        if is_authenticated:
            oauth2authenticated = isinstance(request.successful_authenticator, OAuth2Authentication)

        token_has_scope = TokenHasReadWriteScope()
        return (is_authenticated and not oauth2authenticated) or token_has_scope.has_permission(request, view)