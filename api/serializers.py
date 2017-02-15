"""
This is a doc for Serializers.
"""
from rest_framework import serializers
from django.contrib.auth.models import User as UserAdmin
from django.contrib.auth.models import Group

from api.models import User
# from xingu.models import Product
# from xingu.models import Portal
# from xingu.models import Client
# from xingu.models import DeliveryOrder
from api.validators import passowrd_validation


class UserSerializer(serializers.ModelSerializer):
    """
        This class is a user serializer.
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30, validators=[passowrd_validation])

    class Meta:
        model = User
        fields = ('pk', 'name', 'email', 'profile', 'password', 'is_active')

    def update(self, instance, validated_data):
        """
        Method to update an user.
        """
        instance = super(UserSerializer, self).update(instance, validated_data)
        user = UserAdmin.objects.get(username=instance.user)
        group = Group.objects.get(name=validated_data['profile'])
        user.groups.clear()
        user.groups.add(group)
        if u"password" in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return instance

    def to_representation(self, instance):
        """
        Method defines the JSON.
        """
        if isinstance(instance, User):
            user = UserAdmin.objects.get(username=instance.user)
            return {
                'pk': instance.id,
                'name': instance.name,
                'email': user.email,
                'profile': instance.profile,
                'perms': user.get_all_permissions(),
                'is_active': instance.is_active
            }
        else:
            return {
                'name': instance['name'],
                'email': instance['email'],
                'profile': instance['profile'],
                'password': instance['password'],
                'is_active': instance['is_active']
            }

#
# class ProductSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     This class is a product serializer.
#     """
#
#     class Meta:
#         model = Product
#         fields = ('serial_number', 'model', 'situation', 'is_active')
#
#     def to_representation(self, instance):
#         if isinstance(instance, Product):
#             return {
#                 'pk': instance.pk,
#                 'serial_number': instance.serial_number,
#                 'model': instance.model,
#                 'situation': instance.situation,
#                 'is_active': instance.is_active
#             }
#         else:
#             return {
#                 'serial_number': instance['serial_number'],
#                 'model': instance['model'],
#                 'situation': instance['situation'],
#                 'is_active': instance['is_active']
#             }
#
#
# class PortalSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     This class is a portal serializer.
#     """
#
#     class Meta:
#         model = Portal
#         fields = ('id_portal', 'certificate', 'situation', 'is_active')
#
#     def to_representation(self, instance):
#         if isinstance(instance, Portal):
#             return {
#                 'pk': instance.pk,
#                 'id_portal': instance.id_portal,
#                 'certificate': instance.certificate,
#                 'situation': instance.situation,
#                 'is_active': instance.is_active
#             }
#         else:
#             return {
#                 'id_portal': instance['id_portal'],
#                 'certificate': instance['certificate'],
#                 'situation': instance['situation'],
#                 'is_active': instance['is_active']
#             }
#
#
# class DeliveryOrderSerializer(serializers.ModelSerializer):
#     """
#     This class is a Delivery Order Serializer
#     """
#     products = serializers.ListField()
#
#     class Meta:
#         model = DeliveryOrder
#         fields = ('delivery_note', 'client', 'delivery_date', 'portal', 'move',
#                   'situation', 'is_active', 'products')
#
#     def to_representation(self, instance):
#         if isinstance(instance, DeliveryOrder):
#             products = []
#             for product in instance.product_set.all():
#                 products.append(ProductSerializer(product).data)
#
#             return {
#                 'pk': instance.pk,
#                 'delivery_note': instance.delivery_note,
#                 'client': ClientSerializer(instance.client).data,
#                 'address': (instance.client.address,
#                             instance.client.number,
#                             instance.client.complement,
#                             instance.client.city,
#                             instance.client.state,
#                             instance.client.country,
#                             instance.client.cep),
#                 'delivery_date': instance.delivery_date,
#                 'open_date': instance.open_date,
#                 'portal': PortalSerializer(instance.portal).data,
#                 'move': instance.move,
#                 'situation': instance.situation,
#                 'is_active': instance.is_active,
#                 'products': products
#             }
#         else:
#             return {
#                 'delivery_note': instance['delivery_note'],
#                 'client': ClientSerializer(instance['client']).data,
#                 'address': (instance['client'].address,
#                             instance['client'].number,
#                             instance['client'].complement,
#                             instance['client'].city,
#                             instance['client'].state,
#                             instance['client'].country,
#                             instance['client'].cep),
#                 'delivery_date': instance['delivery_date'],
#                 'portal': PortalSerializer(instance['portal']).data,
#                 'move': instance['move'],
#                 'situation': instance['situation'],
#                 'is_active': instance['is_active'],
#                 'products': instance['products']
#             }
#
#
# class ClientSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     This class is a client serializer.
#     """
#
#     class Meta:
#         model = Client
#         fields = ('name', 'cnpj', 'cep', 'address', 'number',
#                   'complement', 'state', 'city', 'district',
#                   'country', 'latitude', 'longitude', 'situation', 'is_active')
#
#     def to_representation(self, instance):
#         if isinstance(instance, Client):
#             return {
#                 'pk': instance.pk,
#                 'name': instance.name,
#                 'cnpj': instance.cnpj,
#                 'cep': instance.cep,
#                 'address': instance.address,
#                 'number': instance.number,
#                 'complement': instance.complement,
#                 'state': instance.state,
#                 'city': instance.city,
#                 'district': instance.district,
#                 'country': instance.country,
#                 'latitude': instance.latitude,
#                 'longitude': instance.longitude,
#                 'situation': instance.situation,
#                 'is_active': instance.is_active
#             }
#         else:
#             return {
#                 'name': instance['name'],
#                 'cnpj': instance['cnpj'],
#                 'cep': instance['cep'],
#                 'address': instance['address'],
#                 'number': instance['number'],
#                 'complement': instance['complement'],
#                 'state': instance['state'],
#                 'city': instance['city'],
#                 'district': instance['district'],
#                 'country': instance['country'],
#                 'latitude': instance['latitude'],
#                 'longitude': instance['longitude'],
#                 'situation': instance['situation'],
#                 'is_active': instance['is_active']
#             }
