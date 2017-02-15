"""
This is a User View Controller to Web Service.
"""
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User as UserAdmin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.models import User
from api.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Allows CRUD operations over users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @method_decorator(permission_required('xingu.list_user', raise_exception=True))
    def list(self, request):
        return ModelViewSet.list(self, request)

    @method_decorator(permission_required('xingu.add_user', raise_exception=True))
    def create(self, request):
        return ModelViewSet.create(self, request)

    def perform_create(self, serializer):
        data = serializer.data
        User.create(data['name'], data['email'],
                    data['profile'], data['password'],
                    data['is_active'])

    def retrieve(self, request, pk=None):
        if request.user.has_perm('xingu.list_user') or request.user.user.pk == int(pk):
            return ModelViewSet.retrieve(self, request, pk=pk)
        else:
            raise PermissionDenied

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        data = request.data

        if user.user.email != data['email']:
            raise PermissionDenied

        if 'profile' in data:
            if (user.profile != data['profile']) and (data['profile'] == User.ADMINISTRATOR):
                raise PermissionDenied

        if request.user.user.pk == int(pk):
            return self._update_self(request, pk)

        else:
            raise PermissionDenied

    def _update_self(self, request, user_id=None):
        """
        Updates itself
        """
        user = User.objects.get(pk=user_id)
        data = request.data
        partial = False

        if 'profile' in data:
            if user.profile != data['profile']:
                raise PermissionDenied
        else:
            partial = True

        if 'is_active' in data:
            if data['is_active'] == str(False):
                raise PermissionDenied
        else:
            partial = True

        return ModelViewSet.update(self, request, user_id, partial=partial)

    @method_decorator(permission_required('xingu.delete_user', raise_exception=True))
    def destroy(self, request, pk=None):
        if request.user.user.pk == int(pk):
            raise PermissionDenied
        return ModelViewSet.destroy(self, request, pk=pk)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        dic = self.request.query_params
        query = {}
        if 'search' in dic.keys():
            query_name = {'name__contains': dic['search']}
            result_name = User.objects.filter(**query_name)

            query_profile = {'profile__contains': dic['search']}
            result_profile = User.objects.filter(**query_profile)

            query_email = {'user': UserAdmin.objects.filter(
                email__contains=dic['search'])}
            result_email = User.objects.filter(**query_email)

            return result_name | result_profile | result_email

        if 'name' in dic.keys():
            query['name__contains'] = dic['name']
        if 'profile' in dic.keys():
            query['profile__contains'] = dic['profile']
        if 'email' in dic.keys():
            query['user'] = UserAdmin.objects.filter(
                email__contains=dic['email'])
        if 'is_active' in dic.keys():
            query['is_active'] = (dic['is_active'] == 'True')

        return User.objects.filter(**query)


def jwt_response_payload_handler(token, user=None, request=None):
    """
        This method is an override of JWT that returns the token and user permissions.
    """
    instance = User.objects.get(user=user)
    return {
        'user': {
            'pk': instance.id,
            'name': instance.name,
            'email': user.email,
            'profile': instance.profile,
            'is_active': instance.is_active
        },
        'perms': user.get_all_permissions(),
        'token': token,
    }
