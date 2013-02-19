from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _


class Attachment(models.Model):
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
    object_hash = models.CharField(max_length=100, editable=False, verbose_name=_(u'Hash'))
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
        ordering = ('position', )

    def __unicode__(self):
        return self.object_file.url

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.get_next_position()
        self.write_object_hash(False)
        super(Attachment, self).save(*args, **kwargs)

    def get_next_position(self):
        # if position is not given, set it to max for that content_type and object_type plus 1
        _same_type_objects = Attachment.objects.filter(group=self.group,
            content_type=self.content_type)
        return (_same_type_objects.aggregate(p=models.Max('position'))['p'] or 0) + 1

    def calculate_object_hash(self):
        import hashlib
        h = hashlib.sha1()
        h.update(self.object_file.file.read())
        return h.hexdigest()

    def write_object_hash(self, save=True):
        self.object_hash = self.calculate_object_hash()
        if save:
            self.save()


class ObjectAttachable(models.Model):
    attachments = GenericForeignKey(Attachment)

    class Meta:
        abstract = True

    def main_image(self):
        try:
            return self.attachments.filter(object_type='image')[0]
        except:
            return None

    def images(self):
        return self.attachments.filter(object_type='image')

    def downloadables(self):
        return self.attachments.filter(object_type='download')
