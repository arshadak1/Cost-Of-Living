from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
PER_CHOICES = [
    ("month", "month"),
    ("year", "year"),
    ("week", "week"),
    ("day", "day"),
    ("once", "once"),
]

SOURCE_CHOICES = [
    ("Income", "Income"),
    ("Expense", "Expense"),
]

class Data(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=False, verbose_name='Source')
    value = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Amount')
    is_expense = models.CharField(max_length=20, null=True, blank=False, verbose_name='Type', choices=SOURCE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    Date = models.DateField(default=now)
    per = models.CharField(
        max_length = 20,
        choices = PER_CHOICES,
        default = 'month'
        )
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['is_expense','Date']


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    review_text_box = models.TextField(verbose_name='Comment')
    review_rate = models.IntegerField(verbose_name='User Rating')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.review_rate} - {self.created}'

    class Meta:
        ordering = ['user','review_rate']