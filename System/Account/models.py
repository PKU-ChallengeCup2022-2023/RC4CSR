from django.db import models
from django.contrib.auth.models import User

# Create your models here.

__all__ = [
    "PlatformUser",
]

class PlatformUserManager(models.Manager):
    def get_by_user(self, user: User):
        result: PlatformUser = self.get(uid=user)
        return result

class PlatformUser(models.Model):
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    
    uid = models.OneToOneField(to=User, on_delete=models.CASCADE)

    nickname = models.CharField("昵称", null=True, unique=True, max_length=20)
    class Gender(models.IntegerChoices):
        MALE = (0, "男")
        FEMALE = (1, "女")

    gender = models.SmallIntegerField("性别", choices=Gender.choices)

    class Major(models.IntegerChoices):
        CHINESE = (0, "汉语言")
        FOREIGN = (1, "外国语")
        SOCIAL = (2, "社会学")
        POLITICAL = (3, "政治学")
        HISTORY = (4, "历史学")
        MATH = (5, "数学")
        PHYSICS = (6, "物理学")
        CHEMISTRY = (7, "化学")
        BIOLOGY = (8, "生物学")
        COMPUTER = (9, "计算机科学")
        PHILOSOPHY = (10, "哲学")
        PHYCHOLOGY = (11, "心理学")
        OTHERS = (12, "其他")

    major = models.SmallIntegerField("专业", choices=Major.choices, default=Major.OTHERS)

    type_preference = models.ManyToManyField(to="Recommendation.Book_Tag", verbose_name="书籍类型偏好")
    
    def __str__(self) -> str:
        return self.nickname

    def get_type(self=None) -> str:
        '''User一对一模型的必要方法'''
        return "PlatformUser"

    def get_user(self) -> User:
        '''User一对一模型的必要方法'''
        return self.uid

    def get_display_name(self) -> str:
        '''User一对一模型的必要方法'''
        return self.nickname

