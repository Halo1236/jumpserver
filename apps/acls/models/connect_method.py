from django.db import models
from django.utils.translation import gettext_lazy as _

from common.db.fields import JSONManyToManyField
from .base import UserBaseACL

__all__ = ['ConnectMethodACL']


class ConnectMethodACL(UserBaseACL):
    connect_methods = models.JSONField(default=list, verbose_name=_('Connect methods'))
    assets = JSONManyToManyField('assets.Asset', default=dict, verbose_name=_('Assets'))

    class Meta(UserBaseACL.Meta):
        verbose_name = _('Connect method acl')
        abstract = False
