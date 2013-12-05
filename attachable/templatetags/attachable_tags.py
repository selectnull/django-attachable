from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Attachment

from collections import defaultdict


register = template.Library()


class AttachmentNode(template.Node):
    def __init__(self, obj, output_name):
        self.obj = template.Variable(obj)
        self.output_name = output_name

    def render(self, context):
        obj = self.obj.resolve(context)
        content_type = ContentType.objects.get_for_model(obj)
        data = Attachment.objects.select_related().\
            filter(object_id=obj.pk, content_type=content_type).\
            order_by('group', 'position')
        result = defaultdict(list)
        for x in data:
            result[x.group].append(x)
            
        context[self.output_name] = result
        return ''

@register.tag
def get_attachments(parser, token):
    """
    {% get_attachments obj as output_name %}

    """
    try:
        tag_name, obj, _as, output_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('{} tag takes exactly 3 arguments'.format(tag_name))
    return AttachmentNode(obj, output_name)
