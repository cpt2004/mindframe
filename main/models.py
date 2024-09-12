from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    posttime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updatetime','-posttime']

    def __str__(self) -> str:
        return f"{self.topic} by {self.user}"