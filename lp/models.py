from django.db import models


class PhoneSubmission(models.Model):
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.phone} @ {self.created_at:%Y-%m-%d %H:%M:%S}"
