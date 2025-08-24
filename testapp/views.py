

from django.http import JsonResponse, HttpResponse
from .models import TestRecord

def health(request):
	return JsonResponse({'status': 'ok'})

def test_hello(request):
	return HttpResponse('Hello, world!')

def test_json(request):
	return JsonResponse({'message': 'This is a test JSON response.'})

# Create your views here.

def root(request):
	return JsonResponse({"message": "Welcome to the root endpoint!"})


# Simple DB test view
def test_db(request):
	# Create a record
	obj = TestRecord.objects.create(name="Test User")
	# Fetch the latest record
	latest = TestRecord.objects.latest('created_at')
	return JsonResponse({
		"id": latest.id,
		"name": latest.name,
		"created_at": latest.created_at.isoformat(),
	})
