from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:  # 기타사항을 적음
        abstract = True  # model 이지만 데이터베이스에 나타나지 않음 이 모델을 통해 확장시킨 모델을 사용할거라서
