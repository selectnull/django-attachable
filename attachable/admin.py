from django.contrib import contenttypes
from .models import Attachment


class AttachmentInline(contenttypes.generic.GenericStackedInline):
    model = Attachment
    extra = 0
    ct_field = 'content_type'
    fk_field = 'object_id'

    fieldsets = (
        (None, {
            'fields': (('object_file', 'object_type', 'group', 'position', ), ),
        }),
        (None, {
            'fields': ('title', 'alt_title', ),
        }),
    )
