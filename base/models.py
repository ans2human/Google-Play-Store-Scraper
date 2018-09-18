from django.db import models


class BaseModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``timestamp_created`` and ``timestamp_updated`` fields.
    """

    timestamp_created = models.DateTimeField(
        auto_now_add=True
    )

    timestamp_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
