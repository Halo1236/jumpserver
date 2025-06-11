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

    @classmethod
    def _get_filter_queryset(cls, user=None, asset=None, **kwargs):
        queryset = cls.objects.all()
        q = models.Q()
        if asset:
            q &= cls.assets.get_filter_q(asset)
        if user:
            q &= cls.users.get_filter_q(user)
        if kwargs:
            q &= models.Q(**kwargs)
        queryset = queryset.filter(q)
        return queryset.valid().distinct()

    @classmethod
    def filter_queryset(cls, asset=None, **kwargs):
        return cls._get_filter_queryset(asset=asset, **kwargs)
