# -*- coding: utf-8 -*-
#
from rest_framework_bulk import BulkModelViewSet

from common.permissions import IsValidUser
from common.utils import get_logger
from ..models import CustomLabel
from .. import serializers

logger = get_logger(__file__)
__all__ = ['CustomLabelViewSet']


class CustomLabelViewSet(BulkModelViewSet):
    model = CustomLabel
    permission_classes = (IsValidUser,)
    filterset_fields = ("id", "value")
    search_fields = filterset_fields
    serializer_class = serializers.CustomLabelSerializer



    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 权限的限制
        # queryset = CustomLabel.objects.filter(user=self.request.user)
        queryset = CustomLabel.objects
        return queryset
