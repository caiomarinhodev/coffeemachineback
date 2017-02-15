from __future__ import unicode_literals

import moneyed
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField, MoneyPatched
from django.contrib.auth.models import User as UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
import hashlib
import base64


class TimeStamped(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# Create your models here.
class User(TimeStamped):
    """
    Model of user.
    Each user may realize specifics functions, depends of your profile.
     - Only administrator can active an user. User inactive has your data in the system.
    """

    ADMINISTRATOR = 'ADMINISTRATOR'
    MANAGER = 'MANAGER'
    OPERATOR = 'OPERATOR'
    USER = 'USER'
    PROFILES = (
        (ADMINISTRATOR, _('ADMINISTRATOR')),
        (MANAGER, _('MANAGER')),
        (OPERATOR, _('OPERATOR')),
        (USER, _('USER')),
    )
    user = models.OneToOneField(UserAdmin, )
    name = models.CharField(max_length=100, verbose_name=_('name'))
    profile = models.CharField(max_length=20, choices=PROFILES,
                               verbose_name=_('profile'))
    is_active = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ("list_user", "Can list existing users"),
            # ("change_enrollment", "Can change enrollment"),
            # ("change_situation", "Can change situation"),
            # ("approved_portal", "Can create Portals with situation approved"),
            # ("approve_deliveryorder",
            #  "Can create Delivery Order with situation approved and approve them"),
            # ("approve_client",
            #  "Can create Client with situation approved"),
        )

    @staticmethod
    def create(name, email, profile, password, is_active):
        """
        Create an user
        """
        user = User()
        user.name = name
        user.profile = profile
        user.is_active = is_active
        user_admin = UserAdmin.objects.create_user(
            create_username(email), email, password)
        group = Group.objects.get(name=profile)
        user_admin.groups.add(group)
        user_admin.save()
        user.user = user_admin
        user.save()
        
    
class Capsule(TimeStamped):
    """
    Capsule model.
    """

    flavor = models.CharField(max_length=100)
    price_cost = MoneyField(max_digits=10, decimal_places=2, validators=[MinValueValidator(MoneyPatched(0, 'BRL'))])
    price_sale = MoneyField(max_digits=10, decimal_places=2, validators=[MinValueValidator(MoneyPatched(0, 'BRL'))])
    cod_vendor = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def create(flavor, price_cost, price_sale, cod_vendor, is_active):
        """
        Create a capsule.
        """
        capsule = Capsule()
        capsule.flavor = flavor
        capsule.is_active = is_active
        capsule.save()
        return capsule



def create_username(email):
    """
    Create a username to an email hash.
    """
    return base64.urlsafe_b64encode(hashlib.sha1(email).digest())