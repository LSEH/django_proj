from django.db import models
from django.conf import settings

class Content(models.Model):
    drama = '드라마'
    action = '액션'
    thriller = '스릴러'
    romance = '로맨스'
    mystery = '미스테리'
    sf = 'SF'
    genrn_choices = [
        (drama, '드라마'),
        (action, '액션'),
        (thriller, '스릴러'),
        (romance, '로맨스'),
        (mystery, '미스테리'),
        (sf, 'SF'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField()
    genre = models.CharField(max_length=10, choices=genrn_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)