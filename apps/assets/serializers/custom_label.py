# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import CustomLabel


class CustomLabelSerializer(BulkOrgResourceModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CustomLabel
        fields = ['id', 'value', 'user', 'assets']

class CustomLabelDistinctSerializer(BulkOrgResourceModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = CustomLabel
        fields = ("value")

    @staticmethod
    def get_value(obj):
        custom_labels = CustomLabel.objects.filter(name=obj["value"])
        return ', '.join([custom_label.value for custom_label in custom_labels])
