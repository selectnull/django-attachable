from django.contrib import admin
from django.conf import settings
from django.contrib import contenttypes


class ObjectAttachmentInline(contenttypes.generic.GenericStackedInline):
    model = ObjectAttachment
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
