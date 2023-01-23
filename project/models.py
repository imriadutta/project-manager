from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    is_admin = models.IntegerField(default=0, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=13, null=True)
    company = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username


class Project(models.Model):
    pname = models.CharField(max_length=20)
    description = models.TextField(max_length=2000)
    service_type = models.CharField(max_length=1)
    accessed = models.CharField(max_length=7)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=True)
    last_changes = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pname
