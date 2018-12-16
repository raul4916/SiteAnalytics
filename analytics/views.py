from django.shortcuts import render

# Create your views here.
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from analytics.models import *

from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

import json


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

@permission_classes([AllowAny])
@authentication_classes([])
class TrackView(APIView):

	def post(self, request: HttpRequest):

		raw = request.body.decode('UTF-8')
		request = json.loads(raw)

		user_events = ['conversion']
		page_impression_type = ['personalized', 'control']

		requirements = [
			'visitor_token',
			'event_type',
			'payload'
			]

		page_event_reqs = [
			'url',
			'impression_token',
			'session_token',
			'impression_type'
			]

		user_event_reqs = [
			'impression_token',
			'event_name'
			]

		if not self.validate_params(request, requirements):
			return HttpResponse(json.dumps({ "response":"Invalid Params" }),
								content_type = 'application/json', status = 422)

		payload = request['payload']
		if request['event_type'] == 'page_view':
			if not self.validate_params(payload, page_event_reqs):
				return HttpResponse(json.dumps({ "response":"Invalid Params" }),
									content_type = 'application/json', status = 422)
			if not payload['impression_type'] in page_impression_type:
				return HttpResponse(json.dumps({ "response":"Invalid Params" }),
									content_type = 'application/json', status = 422)

			track = Track.objects.create(visitor_token = request['visitor_token'], event_type = request['event_type'])
			PageEvent.objects.create(url = payload['url'], track = track,
									 impression_token = payload['impression_token'],
									 session_token = payload['session_token'],
									 impression_type = payload['impression_type'],
									 elapsed_time_in_ms = payload['elapsed_time_in_ms'])


		elif request['event_type'] == 'user_event':
			if not self.validate_params(payload, user_event_reqs):
				return HttpResponse(json.dumps({ "response":"Invalid Params" }),
									content_type = 'application/json', status = 422)
			if not payload['event_name'] in user_events:
				return HttpResponse(json.dumps({ "response":"Invalid Params" }),
									content_type = 'application/json', status = 422)

			track = Track.objects.create(visitor_token = request['visitor_token'], event_type = request['event_type'])
			UserEvent.objects.create(track = track, impression_token = payload['impression_toke n'],
									 event_name = payload['event_name'])

		else:
			return HttpResponse(
					{ "error":"Missing params" },
					content_type = 'application/json', status = 422)
		return HttpResponse()

	@staticmethod
	def validate_params(arr, requirements):
		for req in requirements:
			if req not in arr:
				return False
		return True


@permission_classes([AllowAny])
@authentication_classes([])
class Report(APIView):

	def get_pages_info(self):
		conversion_total = UserEvent.objects.filter(event_name = 'conversion').count()
		highest_views = PageEvent.objects.values('url').annotate(total_count = models.Count('url')).order_by(
				'-total_count')
		most_time = PageEvent.objects.values('url').annotate(avg_time = models.Avg('elapsed_time_in_ms')).order_by(
				'-avg_time')
		list_conversion = [{ 'url':obj['url'], 'cvr_rate':(conversion_total / obj['total_count']) } for obj in
						   list(highest_views)],

		response = json.dumps({
			'pages':{
				"highest_views"     :list(highest_views), "most_time":list(most_time),
				'highest_conversion':list_conversion
				}
			})
		return HttpResponse(
				response, content_type = 'application/json')

	def reports_visitors(self):
		average_time_per_page = PageEvent.objects.aggregate(average_time_per_page = models.Avg('elapsed_time_in_ms'))
		average_pages_per_session = PageEvent.objects.values('session_token').annotate(count_pages = models.Count('url')).aggregate(average_pages_per_session =models.Avg('count_pages'))
		average_time_per_session = PageEvent.objects.values('session_token').aggregate(
				average_time_per_session = models.Avg('elapsed_time_in_ms'))

		response = json.dumps({
			'visitors':{
				'average_time_per_session' :average_time_per_session['average_time_per_session'],
				'average_time_per_page'    :average_time_per_page['average_time_per_page'],
				'average_pages_per_session':average_pages_per_session['average_pages_per_session']
				}
			});

		return HttpResponse(response,content_type = 'application/json')
