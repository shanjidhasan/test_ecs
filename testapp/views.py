
from django.http import JsonResponse, HttpResponse

def health(request):
	return JsonResponse({'status': 'ok'})

def test_hello(request):
	return HttpResponse('Hello, world!')

def test_json(request):
	return JsonResponse({'message': 'This is a test JSON response.'})

# Create your views here.
