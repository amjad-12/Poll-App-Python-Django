from django.db import models
from django.conf import settings
from django.contrib import admin


class Poll(models.Model):
    question = models.CharField(max_length=55)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice = models.CharField(max_length=55)

    def __str__(self):
        return self.choice


class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

        
    class Meta:
        unique_together = ("poll", "voted_by")

class Customer(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    
    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def username(self):
        return self.user.username

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name









