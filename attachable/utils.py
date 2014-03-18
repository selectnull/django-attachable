from django.contrib import admin
from .admin import AttachmentInline


def add_inline(model, model_admin):
    if not 'inlines' in model_admin.__dict__:
        model_admin.inlines = ()
    model_admin.inlines += (AttachmentInline, )

    admin.site.unregister(model)
    admin.site.register(model, model_admin)
