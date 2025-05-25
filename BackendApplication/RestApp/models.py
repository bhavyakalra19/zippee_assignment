from django.contrib.auth.models import AbstractUser
from django.db import models

#inherited AbstractUser class and modified it by addinf roles field
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        OWNER = 'OWNER', 'owner'
        OTHER = 'OTHER', 'other'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.OTHER
    )

    def __str__(self):
        return f"{self.username} => {self.role}"

#model for Task
class TaskModel(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



#admin user token
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODI1NjU3NywiaWF0IjoxNzQ4MTcwMTc3LCJqdGkiOiI0NDIyNWU1OTAxNzU0ZjdmYmY0N2E1MmJmY2ZkMDQ1OCIsInVzZXJfaWQiOjEsInJvbGUiOiJBRE1JTiJ9.lOetQ-OW7BaW-fIaeKnyIx23JSED4CmAKjPX7RMP7Ko",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4MTc5MjI4LCJpYXQiOjE3NDgxNzAxNzcsImp0aSI6ImRjYmU4NWFhNjA1NzQwNzA4MDYyMTg0OWYxZDZjODYzIiwidXNlcl9pZCI6MSwicm9sZSI6IkFETUlOIn0.lFg_KpZA-v0TsPYpmZuVoCzGMi8_-S9ANOMOOEmIfB8"
# }

#other role token
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODI2MjI3MiwiaWF0IjoxNzQ4MTc1ODcyLCJqdGkiOiIyMzgxOTA4NTdhN2I0ODllOWIxNDIxYTFhZWQ3YWM1OSIsInVzZXJfaWQiOjJ9.6CfQHoFj_AYWa5WH3xHGoK_AhP7YVeihc0HG_0Ordlo",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4MTk0MDc4LCJpYXQiOjE3NDgxNzU4NzIsImp0aSI6ImRmNzczYzlkOGFiNzQ2Y2ZhODg1YWZkNDgyOWUzOGZiIiwidXNlcl9pZCI6Mn0.NysyCAVffHlUxOA97lKWCH5HVSkbzxKPjixYBzx6FKQ"
# }

#OWNER
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODI3NjQyOSwiaWF0IjoxNzQ4MTkwMDI5LCJqdGkiOiIyMmFjYzQwZTJiNDE0YmM5OTFiN2EzZWI4ZmE5NDFjMSIsInVzZXJfaWQiOjQsInJvbGUiOiJPV05FUiJ9.vqyK3YETEmWhH3AV809wmQ-zU9cbw2bj16eWFpUBmHQ",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4MTkzNjI5LCJpYXQiOjE3NDgxOTAwMjksImp0aSI6Ijc3YTY4NjJhNjJlYTQ1N2Y4ZWJkNDMxYmU3NTU0YzZiIiwidXNlcl9pZCI6NCwicm9sZSI6Ik9XTkVSIn0.NyykTvAtxZkeVAgr1Iv2N-voaFxYAUrvrivo3QmUo0M"
# }