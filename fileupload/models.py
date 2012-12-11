from django.db import models
import os, os.path

class Document(models.Model):
    docfile = models.FileField(upload_to='./')

    def delete(self, *args, **kwargs):
            storage, path = self.docfile.storage, self.docfile.path
            super(Document, self).delete(*args, **kwargs)
            storage.delete(path)

    def save(self, *args, **kwargs):
        if self.id is not None:
            a = Document.objects.get(id=self.id)
            os.remove(a.docfile.path)        
        super(Document, self).save(*args, **kwargs)

    def __unicode__(self):
                return str(self.docfile)