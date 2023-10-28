# -*- coding: utf-8 -*-
#
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.utils import lazyproperty
from orgs.mixins.models import JMSOrgBaseModel

__all__ = ['CustomLabel']


class CustomLabel(JMSOrgBaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('value'))

    class Meta:
        unique_together = ('user',)
        verbose_name = _("Custom Labels")

    @classmethod
    def get_user_custom_labels_asset_ids(cls, user):
        return cls.objects.filter(user=user).values_list('asset', flat=True)

    def __str__(self):
        return '%s' % self.value

    @classmethod
    def get_queryset_group_by_value(cls):
        values = cls.objects.values_list('value', flat=True)
        for value in values:
            yield value, cls.objects.filter(value=value)

    class Meta:
        db_table = "assets_customlabel"
        unique_together = [('value')]
        verbose_name = _('Custom Labels')
