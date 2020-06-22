from django.db import models
from uuid import uuid4
from django.utils import timezone


class LeaderBoard(models.Model):
    board_data = models.TextField(null=False)
    board_name = models.CharField(max_length=50)
    board_access_code = models.CharField(max_length=100)
    board_id = models.UUIDField(primary_key=True)
    sort_by_key = models.CharField(default='Points', max_length=100)
    upload_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def generate_key(self):
        self.board_id = uuid4().hex

    def update_form(self):
        self.last_update = timezone.now()

    def __str__(self):
        return self.board_name
