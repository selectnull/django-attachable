from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Attachment

from collections import defaultdict


register = template.Library()


@register.assignment_tag
def get_attachments(obj, count=None, group=None, object_type=None):
    filters = {}

    if count:
        count = int(count)
    if group:
        filters['group'] = group
    if object_type:
        filters['object_type'] = object_type

    content_type = ContentType.objects.get_for_model(obj)
    data = Attachment.objects.select_related().\
        filter(content_type=content_type, object_id=obj.pk, **filters).\
        order_by('group', 'position')

    if data:
        return data if not count else data[:count] if count > 1 else data[0]
    return None
