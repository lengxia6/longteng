from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.views import generic

from .models import Project, HttpApi



# Create your views here.

@login_required
def index(request):
    return render(request,"index.html")
    

def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            msg = "账号或密码错误"
            return render(request,"login.html",{"msg": msg})


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

class ProjectListView(LoginRequiredMixin, generic.ListView):
    """
    项目列表视图 
    """
    model = Project
    template_name ='project/project_list.html'
    paginate_by = 5
    


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """
    项目详细视图
    """
    model = Project
    template_name = "project/project_detail.html"
    

@login_required
def project_edit(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        if project.member is None:
            project.member=""
        else:
            project.member = project.member.replace(",","\n")
        return render(request, "project/project_form.html",{"project": project})
    if request.method == "POST":
        project = Project.objects.get(id=pk)
        project.name = request.POST.get("project_name")
        project_owner_str = request.POST.get("project_owner")
        try:
            project.owner = User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg = "指定的项目负责人不存在"
            if project.member is None:
                project.member=""
            return render(request, "project/project_form.html",{"project": project, "errmsg": errmsg})

        project.description = request.POST.get("project_description").strip()
        project_member_str = request.POST.get("project_member").strip()
        
        if project_member_str:
            member_list = project_member_str.strip().split("\n")
            for item in member_list:
                username = item.strip()
                try:
                   User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg = "项目成员%s不存在" % username
                    #return HttpResponse(len(project_member_str.strip()))
                    return render(request, "project/project_form.html",{"project": project, "errmsg": errmsg})
            project.member = ','.join(member_list)
        else:
            project.member="" 
        project.save()
        return redirect("project_detail",project.id)


@login_required
def project_create(request):
    if request.method == "GET":
        return render(request, "project/project_form.html")
    if request.method == "POST":
        project_name = request.POST.get("project_name")
        project_owner_str = request.POST.get("project_owner")
        try:
            project_owner = User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg = "指定的项目负责人:%s不存在" % project_owner_str
            return render(request, "project/project_form.html",{"errmsg": errmsg})
        project_description = request.POST.get("project_description").strip()
        project_member_str = request.POST.get("project_member").strip()
        if project_member_str:
            member_list = project_member_str.strip().split("\n")
            for item in member_list:
                username = item.strip()
                try:
                   User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg = "项目成员%s不存在" % username
                    #return HttpResponse(len(project_member_str.strip()))
                    return render(request, "project/project_form.html", {"errmsg": errmsg})
            project_member = ','.join(member_list)
        else:
            project_member=""

        project = Project(name=project_name,owner=project_owner,description=project_description,member=project_member)
        project.save()
        return redirect("project_detail",project.id)


@login_required
def httpapi_create(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        return render(request,"project/httpapi_form.html", {"project": project })
    if request.method == "POST":
        httpapi_project = Project.objects.get(id=pk)
        httpapi_name = request.POST.get("httpapi_name")
        httpapi_description = request.POST.get("httpapi_description")
        httpapi_url = request.POST.get("httpapi_url")
        httpapi_requesttype = request.POST.get("httpapi_requesttype")
        httpapi_requestheader = request.POST.get("httpapi_requestheader")
        httpapi_requestparametertype = request.POST.get("httpapi_requestparametertype")
        httpapi_requestbody = request.POST.get("httpapi_requestbody")
        userupdate= request.user

        httpapi = HttpApi(project=httpapi_project,
                          name=httpapi_name,
                          requestType=httpapi_requesttype,
                          apiurl=httpapi_url,
                          requestParameterType=httpapi_requestparametertype,
                          requestHeader=httpapi_requestheader,
                          requestBody=httpapi_requestbody,
                          userUpdate=userupdate,
                          description=httpapi_description
                          )
        httpapi.save()

        #return HttpResponse("ok")
        return redirect("httpapi_list",httpapi_project.id)

@login_required
def httpapi_list(request, pk):
    project = Project.objects.get(id=pk)
    
    rs = HttpApi.objects.filter(project=project)
    paginator = Paginator(rs, 5)
    page = request.GET.get('page')
    httpapis = paginator.get_page(page)
    return render(request, "project/httpapi_list.html", {"project": project, "objects": httpapis})

@login_required
def httpapi_edit(request, project_id, httpapi_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        return render(request,"project/httpapi_form.html", {"project": project, "object": httpapi })
    if request.method == "POST":

        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        httpapi.name = request.POST.get("httpapi_name")
        httpapi.description = request.POST.get("httpapi_description")
        httpapi.apiurl = request.POST.get("httpapi_url")
        httpapi.requestType = request.POST.get("httpapi_requesttype")
        httpapi.requestHeader = request.POST.get("httpapi_requestheader")
        httpapi.requestParameterType = request.POST.get("httpapi_requestparametertype")
        httpapi.requestBody = request.POST.get("httpapi_requestbody")
        httpapi.userUpdate= request.user
        httpapi.save()
        return redirect("httpapi_list",project.id)
