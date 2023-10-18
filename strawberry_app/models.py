import os

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Culture(BaseModel):
    culture = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.culture}"


class Months(BaseModel):
    month = models.CharField(max_length=15)
    culture = models.ManyToManyField(Culture, related_name="months")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.month}"

    @property
    def culture_names(self):
        return ", ".join([culture.culture for culture in self.culture.all()])


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"


class PlantImage(BaseModel):
    video = models.FileField(upload_to="videos/", blank=True)
    image = models.ImageField(upload_to="profile_pics/", default="default_image.jpg")


class MediaFile(BaseModel):
    file = models.FileField(upload_to="media/")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(MediaFile, self).delete(*args, **kwargs)

    @staticmethod
    def get_all_files():
        media_path = "media"
        return [os.path.join(media_path, f) for f in os.listdir(media_path)]
