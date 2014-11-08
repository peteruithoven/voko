from django.db import models
from django_extensions.db.models import TimeStampedModel
from tinymce.models import HTMLField


class MailTemplate(TimeStampedModel):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default="VOKO Utrecht - ")
    html_body = HTMLField()

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.subject)