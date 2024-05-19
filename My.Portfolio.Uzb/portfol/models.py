from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.

STATUS = (
    ('active',"Active"),
    ('deactive', "Deactive"),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class  Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ('-created_at','status')

    def str(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('article:category_list', args=[self.id,])



class Site(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category', verbose_name="Kategoriya")
    title = models.CharField(max_length=120, verbose_name="info")
    subtitle = models.CharField(max_length=250, verbose_name="Kichik info")
    body = models.TextField(verbose_name="opisaniyasi")
    video = models.FileField(upload_to='post_videos/%Y/%m/%d/', blank=True, null=True, verbose_name="video")
    photo = models.ImageField(upload_to='post_photo/%Y/%m/%d/', blank=True, null=True, verbose_name="photo")
    see = models.PositiveIntegerField(default=100000, verbose_name="👀")

    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sayt"
        verbose_name_plural = "Saytlar"
        ordering = ('-created_at',)

    def str(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail', args=[self.id,])


    
class Comment(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    body = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ("-created_at",)

    def str(self):
        text = f"{self.name}  - {self.email}"
        return text