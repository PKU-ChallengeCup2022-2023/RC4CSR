from django.db import models

from Account.models import PlatformUser

# Create your models here.

__all__ = [
    "Book",
    "Book_Tag",
    "Tags",
    "SearchRecord"
]

Tags = [
        ('文学',(
            (0, '小说'),
            (1, '文学'),
            (2, '外国文学'),
            (3, '经典'),
            (4, '中国文学'),
            (5, '随笔'),
            (6, '日本文学'),
            (7, '散文'),
            (8, '村上春树'),
            (9, '诗歌'),
            (10, '童话'),
            (11, '名著'),
            (12, '儿童文学'),
            (13, '古典文学'),
            (14, '余华'),
            (15, '王小波'),
            (16, '当代文学'),
            (17, '杂文'),
            (18, '张爱玲'),
            (19, '外国名著'),
            (20, '鲁迅'),
            (21, '钱钟书'),
            (22, '诗词'),
            (23, '茨威格'),
            )
         ),
        ('流行', (
            (100, '漫画'),
            (101, '推理'),
            (102, '绘本'),
            (103, '悬疑'),
            (104, '东野圭吾'),
            (105, '科幻'),
            (106, '青春'),
            (107, '言情'),
            (108, '推理小说'),
            (109, '奇幻'),
            (110, '日本漫画'),
            (111, '武侠'),
            (112, '耽美'),
            (113, '科幻小说'),
            (114, '网络小说'),
            (115, '穿越'),
            (116, '轻小说'),
            (117, '魔幻'),
            (118, '青春文学'),
            (119, '校园'),
            )
         ),
        ('文化', (
            (200, '历史'),
            (201, '心理学'),
            (202, '哲学'),
            (203, '社会学'),
            (204, '传记'),
            (205, '文化'),
            (206, '艺术'),
            (207, '社会'),
            (208, '政治'),
            (209, '设计'),
            (210, '政治学'),
            (211, '宗教'),
            (212, '电影'),
            (213, '建筑'),
            (214, '中国历史'),
            (215, '数学'),
            (216, '回忆录'),
            (217, '思想'),
            (218, '人物传记'),
            (219, '国学'),
            (220, '人文'),
            (221, '音乐'),
            (222, '绘画'),
            (223, '西方哲学'),
            (224, '戏剧'),
            (225, '近代史'),
            )
         ),
        ('生活', (
            (300, '爱情'),
            (301, '成长'),
            (302, '生活'),
            (303, '心理'),
            (304, '女性'),
            (305, '旅行'),
            (306, '励志'),
            (307, '教育'),
            (308, '摄影'),
            (309, '职场'),
            (310, '美食'),
            (311, '游记'),
            (312, '灵修'),
            (313, '健康'),
            (314, '情感'),
            (315, '人际关系'),
            )
         ),
        ('经管', (
            (400, '经济学'),
            (401, '管理'),
            (402, '经济'),
            (403, '商业'),
            (404, '金融'),
            (405, '投资'),
            (406, '营销'),
            (407, '理财'),
            (408, '创业'),
            (409, '股票'),
            (410, '广告'),
            )
         ),
        ('科技', (
            (500, '科普'),
            (501, '互联网'),
            (502, '科学'),
            (503, '编程'),
            (504, '交互设计'),
            (505, '算法'),
            (506, '用户体验'),
            (507, '科技'),
            )
         ),
    ]

class Book_Tag(models.Model):
    class Meta:
        verbose_name = "书籍类型"
        verbose_name_plural = verbose_name
    tag_id = models.IntegerField("id", null=True, unique=True)
    book_tag = models.CharField("标签", max_length=20, null=True)
    def __str__(self):
        return self.book_tag

class Book(models.Model):
    bookname = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    # cover = models.ImageField() install Pillow first
    book_tag = models.IntegerField(
        choices=Tags,
        blank=True,
        default=None,
    )
    url = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=50, blank=True)
    publish_time = models.CharField(max_length=20, blank=True)
    comment_num = models.IntegerField(null=True)
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    percent_5 = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    percent_4 = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    percent_3 = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    percent_2 = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    percent_1 = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    def __str__(self) -> str:
        return self.bookname
    

class SearchRecord(models.Model):
    searcher : PlatformUser = models.ForeignKey(
        PlatformUser, on_delete=models.CASCADE, 
        related_name='searcher', default=None, null=True, blank=True
        )
    search_tag = models.IntegerField(
        choices=Tags,
        blank=True,
        default=None,
    )
    search_cont = models.CharField(max_length=50)
    search_time = models.DateTimeField("搜索时间")
    
    

        
        
