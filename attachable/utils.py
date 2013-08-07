from django.contrib import admin
from .admin import AttachmentInline


def add_inline(model, model_admin):
    admin.site.unregister(model)
    model_admin.inlines += (AttachmentInline, )
    admin.site.register(model, model_admin)
