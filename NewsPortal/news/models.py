from typing import Union, Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        rating = Post.objects.filter(post_author=self.pk).aggregate(sum=Sum('post_rating'))['sum'] * 3
        rating += Comment.objects.filter(user=self.user).aggregate(sum=Sum('comment_rating'))['sum']
        rating += Comment.objects.filter(post__post_author=self.pk).aggregate(sum=Sum('comment_rating'))['sum']
        self.author_rating = rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'ar'
    news = 'nw'
    TYPE = [(news, 'News'), (article, 'Article')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPE, default=news)
    post_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating > 0:
            self.post_rating -= 1
            self.save()

    def preview(self):
        return self.post_text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating > 0:
            self.comment_rating -= 1
            self.save()
