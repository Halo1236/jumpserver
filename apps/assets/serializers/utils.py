from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.utils import validate_ssh_private_key, parse_ssh_private_key_str


def validate_password_contains_left_double_curly_bracket(password):
    # validate password contains left double curly bracket
    # check password not contains `{{`
    if '{{' in password:
        raise serializers.ValidationError(_('Password can not contains `{{` '))


def validate_ssh_key(ssh_key, passphrase=None):
    valid = validate_ssh_private_key(ssh_key, password=passphrase)
    if not valid:
        raise serializers.ValidationError(_("private key invalid or passphrase error"))
    return parse_ssh_private_key_str(ssh_key, passphrase)