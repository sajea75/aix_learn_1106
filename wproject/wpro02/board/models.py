from django.db import models

class FishPrediction(models.Model):
    weight = models.FloatField(verbose_name='무게')
    length = models.FloatField(verbose_name='길이')
    diagonal = models.FloatField(verbose_name='대각선')
    height = models.FloatField(verbose_name='높이')
    width = models.FloatField(verbose_name='넓이')
    pred_fish = models.CharField(max_length=50, verbose_name='예측 생선')
    max_proba = models.FloatField(verbose_name='예측 확률')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='예측 일시')

    def __str__(self):
        return f"{self.pred_fish} ({self.max_proba})"