from django.db import models


# {
#   visitor_token: 'b3ee022e-2335-4dbd-90d4-4ea54a89915d',
#   event_type: 'page_view'
#   payload: {
#     url: 'blog.mutinyhq.com/my-sweet-post',
#     impression_token: '444e5991-ac9a-4201-8201-cca5cea923fe',
#     session_token: '20e6e284-c0b2-4be0-8e36-96e63b41af9a',
#     impression_type: 'personalized',
#   }
# }
# Create your models here.


class Track(models.Model):
	visitor_token = models.UUIDField()
	event_type = models.CharField(max_length = 50)


class Event(models.Model):
	track = models.ForeignKey(Track, on_delete = models.PROTECT)
	impression_token = models.UUIDField(max_length = 255)

	class Meta:
		abstract = True


class PageEvent(Event):
	url = models.CharField(max_length = 255)
	impression_type = models.CharField(max_length = 50)
	session_token = models.UUIDField(max_length = 255)
	elapsed_time_in_ms = models.IntegerField()


class UserEvent(Event):
	event_name = models.CharField(max_length = 255)
