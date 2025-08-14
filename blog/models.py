from django.db import models
from django.utils import timezone

class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    used = models.BooleanField(default=False)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 1800