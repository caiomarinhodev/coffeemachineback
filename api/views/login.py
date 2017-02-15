"""
This is a Login View Controller to Web Service.
"""
from django.contrib.auth.models import User
from rest_framework_jwt.views import ObtainJSONWebToken


class LoginView(ObtainJSONWebToken):
    """
    Allow the user login in system
    """

    def post(self, request):
        """
        Handle post requests to login webservice
        :param request: a post request.
        :return: a view.
        """
        data = request.data
        try:
            auth_user = User.objects.get(email=data['username'])
            if not auth_user.user.is_active:
                raise User.DoesNotExist
            username = auth_user.username
        except User.DoesNotExist:
            username = "invalid_username"

        request.data['username'] = username
        return super(LoginView, self).post(request)
