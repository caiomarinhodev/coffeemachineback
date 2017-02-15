"""
This is a Reset Password View Controller to Web Service.
"""
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail.message import EmailMultiAlternatives
from rest_framework import status


class ResetView(APIView):
    """
        Allow the user login in system
    """

    def post(self, request):
        """
            This method post control.
        """
        data = request.data

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            json = {'result': 'User does not exist'}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }

        def send_mail(self, context, from_email, to_email):
            """
            This method send mail to user.
            """

            subject_template_name = "registration/password_reset_subject.txt"
            email_template_name = "registration/password_reset_email.html"
            subject = loader.render_to_string(subject_template_name, context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body = loader.render_to_string(email_template_name, context)
            email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
            email_message.send()

        send_mail(self, context, settings.EMAIL_HOST_USER, data['email'])
        json = {'result': 'Email sent'}
        return Response(json)
