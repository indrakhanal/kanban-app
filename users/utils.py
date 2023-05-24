import re
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import secrets


def validate_email_address(email_address):
   if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address):
       return False
   else:
       return True
   
   
def get_username(email):
    username = email.split('@')[0]
    if User.objects.filter(username=username).exists():
        username += str(secrets.token_hex(2))
        return username
    else:
        return username
   
class AuthenticationFailed(APIException):
    status_code  = status.HTTP_403_FORBIDDEN
    default_detail = _('Incorrect authentication Credential')
    default_code = 'authentication_failed'