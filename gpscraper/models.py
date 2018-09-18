from django.db import models

from base.models import BaseModel


class AppData(BaseModel):

    name =              models.CharField(max_length=255)
    uid =               models.CharField(max_length=255, unique=True)
    dev_name =          models.CharField(max_length=255)
    icon_url =          models.URLField()
    category =          models.CharField(max_length=50)
    description =       models.TextField()
    dev_email =         models.EmailField()
    objects =           models.Manager()

    def __str__(self):
        return '%s' % (self.name, )


class AppSearchIndex(BaseModel):

    query =             models.CharField(max_length=255, unique=True)
    apps =              models.ManyToManyField(AppData)
    objects =           models.Manager()

    def __str__(self):
        return '%s' % (self.query, )
