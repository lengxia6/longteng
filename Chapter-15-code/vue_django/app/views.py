from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Project

import json

# Create your views here.

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({ "code": 200, "msg": "认证成功", "user": {"username":username, "password":password}})
        else:
            return JsonResponse({ "code": 401, "msg": "认证失败"})
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def project_list(request):
    if request.method == "GET":
        page = request.GET.get("page")
        start = int(page) * 20 - 20
        end = int(page) * 20 
        total = Project.objects.count()
        query_data = Project.objects.all()[start:end]
        print(query_data)
        projects_data = []
        for item in query_data:
            data = {}
            data["name"] = item.name
            data["description"] = item.description
            data["owner"] = item.owner.username
            data["id"] = item.id
            projects_data.append(data)
        response_data = {"total": total, "projects": projects_data}
            

        return JsonResponse(response_data)
    else:
        return HttpResponseNotAllowed(["GET"])

@login_required   
@csrf_exempt
def project_edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data["id"]
        project = Project.objects.get(id=id)
        project.name = data["name"]
        project.description = data["description"]
        project.save()
        return JsonResponse({ "code": 200, "msg": "编辑成功"})
    else:
        return HttpResponseNotAllowed(["GET"])

@login_required
@csrf_exempt
def project_add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        owner = request.user
        name = data["name"]
        description = data["description"]
        project = Project(name=name, description=description,owner=owner)
        project.save()
        return JsonResponse({ "code": 200, "msg": "添加成功"})
    else:
        return HttpResponseNotAllowed(["GET"])

@login_required
@csrf_exempt
def project_delete(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data["id"]
        project = Project.objects.get(id=id)
        project.delete()
        return JsonResponse({ "code": 200, "msg": "删除成功"})
    else:
        return HttpResponseNotAllowed(["POST"])



@login_required
@csrf_exempt
def project_batchdelete(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ids = data["ids"].split(",")
        for id in ids:
            project = Project.objects.get(id=id)
            project.delete()
        return JsonResponse({ "code": 200, "msg": "删除成功"})
    else:
        return HttpResponseNotAllowed(["POST"])

