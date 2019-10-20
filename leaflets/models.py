from django.db import models

# Create your models here.


class Leaflet(models.Model):
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='leaflets/')
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title