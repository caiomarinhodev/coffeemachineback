"""coffeemachine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.contrib.auth.views import password_reset_confirm, password_reset_complete

from api.views.login import LoginView
from api.views.reset import ResetView
from api.views.payment import get_session, payment_card

from api.views.user_views import UserViewSet
from api.views.capsule_views import CapsuleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'capsules', CapsuleViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^retorno/pagseguro/', include('pagseguro.urls')),
    url(r'^', include(router.urls)),
    # Tests
    url(r'^get-session/$', get_session),
    url(r'^payment/$', payment_card),
    # BD
    url(r'^login', LoginView.as_view()),
    url(r'^recover', ResetView.as_view()),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete')
]
