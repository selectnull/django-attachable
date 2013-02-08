from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class ObjectAttachment(models.Model):
    OBJECT_TYPE = (
        ('image', _('Image')),
        ('download', _('File for download')),
    )

    # content object fields
    content_type = models.ForeignKey(ContentType,
        related_name='content_type_set_for_%(class)%',
        verbose_name=_('content_type')
    )
    object_id = models.IntegerField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    object_file = models.FileField(upload_to='attachments', verbose_name=_('File'))
    object_type = models.CharField(max_length=10, choices=OBJECT_TYPE, default=OBJECT_TYPE[0][0],
        verbose_name=_('Type'))
    group = models.CharField(max_length=50, blank=True,
        verbose_name=_(u'Group'))
    position = models.IntegerField(blank=True, verbose_name=_('Position'))

    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    alt_title = models.CharField(max_length=200, blank=True, verbose_name=_('Alternative title'))

    class Meta:
        db_table = "object_attachments"
        verbose_name = _(u"Attachment")
        verbose_name_plural = _(u"Attachments")

    def __unicode__(self):
        return self.object_file.url

    def save(self, *args, **kwargs):
        if self.position is None:
            # if position is not given, set it to max for that content_type and object_type plus 1
            _same_type_objects = ObjectAttachment.objects.filter(
                content_type=self.content_type, object_type=self.object_type)
            self.position = (_same_type_objects.aggregate(p=models.Max('position'))['p'] or 0) + 1
        super(ObjectAttachment, self).save(*args, **kwargs)

class ObjectAttachable(models.Model):
    def main_image(self):
        try:
            return self.attachments.filter(object_type='image')[0]
        except:
            return None

    def images(self):
        return self.attachments.filter(object_type='image')

    def downloadables(self):
        return self.attachments.filter(object_type='download')

    class Meta:
        abstract = True
