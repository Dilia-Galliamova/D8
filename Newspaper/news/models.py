from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse

post = 'PS'
news = 'NW'

POST_TYPE = [(post, 'Статья'), (news, 'Новость')]


class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def update_rating(self):
        s1 = self.post_set.aggregate(s=Sum('rating')*3)['s']
        s2 = self.comment_set.aggregate(s=Sum('rating'))['s']
        s3 = self.post_set.aggregate(s=Sum('comment__rating'))['s']
        self.rating = s1 + s2 + s3
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=datetime.now, blank=True)
    type = models.CharField(max_length=2, choices=POST_TYPE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('one_post', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
