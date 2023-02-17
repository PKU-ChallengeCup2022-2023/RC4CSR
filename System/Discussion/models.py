from django.db import models
from django.contrib.auth.models import Group
from Account.models import PlatformUser
from Recommendation.models import Book

# Create your models here.

all = [
    'DiscGroup',
    'DiscRecord'
]


class DiscGroupManager(models.Manager):
    def get_by_group(self, group: Group):
        result: DiscGroup = self.get(uid=group)
        return result

class DiscGroup(models.Model):
    class Meta:
        verbose_name = "讨论组"
        verbose_name_plural = verbose_name
        
    uid = models.OneToOneField(to=Group, on_delete=models.CASCADE)
    groupName = models.CharField("组名", null=True, unique=True, max_length=20)
    disc_center = models.ForeignKey('Recommendation.Book', on_delete=models.CASCADE)
    found_time = models.DateTimeField("创建时间")
    
    founder = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, related_name='founder')
    member1 = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, 
                                related_name='member1', default=None, null=True, blank=True)
    member2 = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, 
                                related_name='member2', default=None, null=True, blank=True)
    member3 = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, 
                                related_name='member3', default=None, null=True, blank=True)
    member4 = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, 
                                related_name='member4', default=None, null=True, blank=True)
    member5 = models.ForeignKey('Account.PlatformUser', on_delete=models.CASCADE, 
                                related_name='member5', default=None, null=True, blank=True)
    
    description = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.groupName
    
class LikeRecord(models.Model):

    class Meta:
        verbose_name = "点赞记录"
        verbose_name_plural = verbose_name

    like_num = models.IntegerField(default=0)
    like_users = models.ManyToManyField(to=PlatformUser)
    
    
class DiscRecord(models.Model):
    class Meta:
        verbose_name = "讨论记录"
        verbose_name_plural = verbose_name
        
    summary = models.CharField(max_length=50, default=None)
    pub_time = models.DateTimeField("发布时间")
    publisher = models.ForeignKey("Account.PlatformUser", on_delete=models.CASCADE)
    belong_to = models.ForeignKey("DiscGroup", on_delete=models.CASCADE)
    reply_to = models.IntegerField("回复", default=0)
    content = models.CharField(max_length=200)
    like = models.OneToOneField(to=LikeRecord, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.summary
    
