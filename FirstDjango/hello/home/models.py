from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True,null=True)
    #content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_posts')


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

class Comment(models.Model):
    posts = models.ForeignKey(post,related_name="comments",on_delete=models.CASCADE)
    name = models.ForeignKey(User,on_delete=CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.posts.title, self.name)
        
    def get_absolute_url(self):
        return reverse('blog-home')

    
    
