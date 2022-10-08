from django.db.models import TextChoices
from .mfa import MFAOtp, MFASms, MFARadius, MFACustom

RSA_PRIVATE_KEY = 'rsa_private_key'
RSA_PUBLIC_KEY = 'rsa_public_key'


class MFAType(TextChoices):
    OTP = MFAOtp.name, MFAOtp.display_name
    SMS = MFASms.name, MFASms.display_name
    Radius = MFARadius.name, MFARadius.display_name
    Custom = MFACustom.name, MFACustom.display_name
