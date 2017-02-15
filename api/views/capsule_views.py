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
from api.models import Capsule, User
from api.serializers import CapsuleSerializer


class CapsuleViewSet(ModelViewSet):
    """
    Allows CRUD operations over users.
    """
    queryset = Capsule.objects.all()
    serializer_class = CapsuleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    # @method_decorator(permission_required('xingu.list_user', raise_exception=True))
    def list(self, request):
        return ModelViewSet.list(self, request)

    # @method_decorator(permission_required('xingu.add_user', raise_exception=True))
    def create(self, request):
        return ModelViewSet.create(self, request)

    def perform_create(self, serializer):
        data = serializer.data
        Capsule.create(data['flavor'], data['price_cost'],
                    data['price_sale'], data['cod_vendor'],
                    data['is_active'])

    def retrieve(self, request, pk=None):
       return ModelViewSet.retrieve(self, request, pk)

    def update(self, request, pk=None):
        product = self.get_object()
        data = request.data
        return ModelViewSet.update(self, request, pk)

    # @method_decorator(permission_required('xingu.delete_user', raise_exception=True))
    def destroy(self, request, pk=None):
        return ModelViewSet.destroy(self, request, pk=pk)

    def get_queryset(self):
        dic = self.request.query_params
        query = {}
        if 'search' in dic.keys():
            query_pricecost = {'price_cost__contains': dic['search']}
            result_pricecost = Capsule.objects.filter(**query_pricecost)

            query_pricesale = {'price_sale__contains': dic['search']}
            result_pricesale = Capsule.objects.filter(**query_pricesale)

            query_codvendor = {'cod_vendor__contains': dic['search']}
            result_codvendor = Capsule.objects.filter(**query_codvendor)

            return result_pricecost | result_pricesale | result_codvendor

        if 'price_cost' in dic.keys():
            query['price_cost__contains'] = dic['price_cost']
        if 'price_sale' in dic.keys():
            query['price_sale__contains'] = dic['price_cost']
        if 'cod_vendor' in dic.keys():
            query['cod_vendor__contains'] = dic['cod_vendor']
        if 'is_active' in dic.keys():
            query['is_active'] = (dic['is_active'] == 'True')

        return Capsule.objects.filter(**query)
