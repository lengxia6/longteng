from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def index(request):
    #return HttpResponse("index")
    try:
        data = json.loads(request.body)
    except:
        return HttpResponse("no json")
    r_data = {"hello": data["name"]}
    return HttpResponse(json.dumps(r_data))
    

@csrf_exempt
def mock(request,product_id):
    if request.method == "GET":
        content = {'id': int(product_id),
              'inStock': True}
        return HttpResponse(json.dumps(content))
    elif request.method == "PUT":
          data = request.body
          return HttpResponse(data)
    elif request.method == "DELETE":
          HttpResponse.status_code = 204
          return HttpResponse()
@csrf_exempt
def mock_post(request):
      if request.method == "POST":
            try:
                json.loads(request.body)
            except Exception as e:
                data = {'msg': e.__repr__() }
                return HttpResponse(json.dumps(data))
            return HttpResponse(request.body)

    

    

