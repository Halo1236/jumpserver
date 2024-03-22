import requests
from rest_framework.decorators import action
from rest_framework.response import Response

from common.exceptions import JMSException
from orgs.mixins.api import OrgBulkModelViewSet
from .common import ACLUserAssetFilterMixin
from .. import models, serializers

__all__ = ['CommandFilterACLViewSet', 'CommandGroupViewSet']


class CommandGroupViewSet(OrgBulkModelViewSet):
    model = models.CommandGroup
    filterset_fields = ('name', 'command_filters')
    search_fields = ('name',)
    serializer_class = serializers.CommandGroupSerializer


class CommandACLFilter(ACLUserAssetFilterMixin):
    class Meta:
        model = models.CommandFilterACL
        fields = ['name', ]


def send_to_jk(js_data):
    headers = {
        'Accept': 'application/json'
    }
    body = {
        'js_data': js_data,
    }
    try:
        # 发送工单信息到金库
        response = requests.post("https://baidu.com", headers=headers, data=body)
        msg = response.json()
    except Exception as error:
        msg = {}
    return msg


class CommandFilterACLViewSet(OrgBulkModelViewSet):
    model = models.CommandFilterACL
    filterset_class = CommandACLFilter
    search_fields = ['name']
    serializer_class = serializers.CommandFilterACLSerializer
    rbac_perms = {
        'command_review': 'tickets.add_superticket'
    }

    @action(['POST'], detail=False, url_path='command-review')
    def command_review(self, request, *args, **kwargs):
        serializer = serializers.CommandReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'run_command': serializer.validated_data['run_command'],
            'session': serializer.session,
            'cmd_filter_acl': serializer.cmd_filter_acl,
            'org_id': serializer.org.id
        }
        ticket = serializer.cmd_filter_acl.create_command_review_ticket(**data)
        info = ticket.get_extra_info_of_review(user=request.user)
        jk_data = send_to_jk(info)
        info['jk_url'] = jk_data.get('url', 'http://localhost:9528')
        return Response(data=info)
