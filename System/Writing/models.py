from django.db import models
from Account.models import PlatformUser
from Discussion.models import LikeRecord

# Create your models here.

__all__ = [
    'Pencraft',
    'Chapter',
]

class Pencraft(models.Model):
    """Pencraft

    :param models: To be completed
    :type models: To be completed
    """
    topic = models.CharField(max_length=100)
    pub_date = models.DateField('date published')
    chap_num = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    # tags = 
    author : PlatformUser = models.ForeignKey(
        PlatformUser, on_delete=models.CASCADE, 
        related_name='author', default=None, null=True, blank=True
        )
    like = models.OneToOneField(to=LikeRecord, on_delete=models.CASCADE, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.topic


class Chapter(models.Model):
    """Chapter

    :param models: _description_
    :type models: _type_
    """

    collection = models.ForeignKey(
        'Pencraft',
        default=None,
        on_delete=models.CASCADE
    )
    chap_name = models.CharField(max_length=100)
    pub_date = models.DateField('date published')
    order_num = models.IntegerField(default=0)
    
    text = models.CharField(max_length=3000)
    
    def __str__(self) -> str:
        return self.chap_name
    
    