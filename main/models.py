from django.db import models

class ContactMessage(models.Model):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    zodiac  = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.zodiac}) — {self.created_at:%Y-%m-%d}"