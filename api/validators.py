"""
Module contains all validators.
"""
from rest_framework import serializers
import re


def passowrd_validation(password):
    """
    Verify if a password is valid.

    Args:
        password (str): Password create by user.

    Note:
        Password must be have at least one letter in upper case, one letter
        in lower case, one number and one symbol.
        Password must be have at least six characters.
    """
    regex1 = r'([!,@,#,$,%,\^,&,*,?,_,~])+'
    regex2 = '([A-Z])+'
    regex3 = '([a-z])+'
    regex4 = '([0-9])+'
    if not (len(password) >= 8 and
            re.search(regex1, password) is not None and
            re.search(regex2, password) is not None and
            re.search(regex3, password) is not None and
            re.search(regex4, password) is not None):
        raise serializers.ValidationError('Password is in invalid format.')
