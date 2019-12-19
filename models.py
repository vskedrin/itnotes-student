from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from mdeditor.fields import MDTextField


def get_sentinel_user():
    return User.objects.get(username='deleted')[0]

# Create your models here.
class GlobalTheme(models.Model):
    name = models.CharField('Тема',max_length=150, blank=True)
    description = models.TextField('Описание', max_length=500, blank=True)

class LocalThemeTree(MPTTModel):
    name = models.CharField('Тема',max_length=150, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = MDTextField()
    author = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        default=1
    )
    

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def items_count(self):
        return self.get_descendant_count()
    # def get_bug_count(self):
    #     return Union.objects.filter(category=self).count()