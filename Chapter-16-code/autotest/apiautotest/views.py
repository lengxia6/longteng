from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_exempt

from django.views import generic

from .models import Project, HttpApi, HttpRunResult, HttpTest, HttpTestResult
import requests
from .lib import utils



# Create your views here.

@login_required
def index(request):
    project_count = Project.objects.all().count()
    httpapi_count = HttpApi.objects.all().count()
    httptest_count = HttpTest.objects.all().count()
    httptestresult_count = HttpTestResult.objects.all().count()
    #return HttpResponse(project)
    return render(request,"index.html", {"project": project_count, "httpapi": httpapi_count,
    "httptest": httptest_count, "httptestresult": httptestresult_count})
    
    

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
        httpapi_assertType = request.POST.get("httpapi_asserttype")
        httpapi_assertContent = request.POST.get("httpapi_assertcontent")
        userupdate= request.user

        httpapi = HttpApi(project=httpapi_project,
                          name=httpapi_name,
                          requestType=httpapi_requesttype,
                          apiurl=httpapi_url,
                          requestParameterType=httpapi_requestparametertype,
                          requestHeader=httpapi_requestheader,
                          requestBody=httpapi_requestbody,
                          userUpdate=userupdate,
                          description=httpapi_description,
                          assertType=httpapi_assertType,
                          assertContent=httpapi_assertContent
                          )
        httpapi.save()

        #return HttpResponse("ok")
        return redirect("httpapi_list",httpapi_project.id)

@login_required
def httpapi_list(request, pk):
    project = Project.objects.get(id=pk)
    
    rs = HttpApi.objects.filter(project=project).order_by("-lastUpdateTime")
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
        httpapi.assertType = request.POST.get("httpapi_asserttype")
        httpapi.assertContent = request.POST.get("httpapi_assertcontent")
        httpapi.userUpdate= request.user
        httpapi.save()
        return redirect("httpapi_list",project.id)


@login_required
def httpapi_run(request, project_id, httpapi_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        response_header = ""
        assertresult = ""
        if httpapi.requestType == "GET":
            data = {}
            if httpapi.requestBody != "":
                for line in httpapi.requestBody.strip().split("\n"):
                    key,value = line.split("=")
                    data[key] = value
                    
            r = requests.get(url=httpapi.apiurl,params=data)
            for item in r.headers:
                response_header += "%s: %s\n" % (item, r.headers.get(item))
            if httpapi.assertType == "noselect":
                assertresult = ""
            elif httpapi.assertType == "in":
                if httpai.assertContent.strip() in r.text:
                    assertresult = "ok"
                else:
                    assertresult = "failed"
            elif httpapi.assertType == "status_code":
                if httpapi.assertContent.strip() == str(r.status_code):
                    assertresult = "ok"
                else:
                    assertresult = "failed"
        if httpapi.requestType == "POST":
            request_header = {}
            if httpapi.requestHeader != "":
                for line in httpapi.requestHeader.strip().split("\n"):
                    key,value = line.split("=")
                    request_header[key] = value
            if httpapi.requestParameterType == "form-data":
                request_body = {}
                for line in httpapi.requestBody.strip().split("\n"):
                    key,value = line.split("=")
                    request_body[key] = value
                r = requests.post(url=httpapi.apiurl,data=request_body,headers=request_header)
            elif httpapi.requestParameterType == "raw":
                request_body = httpapi.requestBody.strip()
                print(request_body)
                r = requests.post(url=httpapi.apiurl,data=request_body,headers=request_header)
            for item in r.headers:
                response_header += "%s: %s\n" % (item, r.headers.get(item))
            if httpapi.assertType == "noselect":
                assertresult = ""
            elif httpapi.assertType == "in":
                if httpai.assertContent.strip() in r.text:
                    assertresult = "ok"
                else:
                    assertresult = "failed"
            elif httpapi.assertType == "status_code":
                if httpapi.assertContent.strip() == str(r.status_code):
                    assertresult = "ok"
                else:
                    assertresult = "failed"
                      
        httprunresult = HttpRunResult(httpapi=httpapi, 
                                      response=r.text, 
                                      header=response_header, 
                                      statusCode = r.status_code,
                                      assertResult = assertresult
                                      )
        httprunresult.save()
        #return HttpResponse("result add ok")
        return redirect("httpapi_result",project.id, httpapi.id)


@login_required
def httpapi_result(request, project_id, httpapi_id):
    project = Project.objects.get(id=project_id)
    httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
    try:
        httpresult = HttpRunResult.objects.filter(httpapi=httpapi).order_by("-id")[0]
    except:
        return render(request,"project/httpapi_result.html", {"project": project})

    return render(request,"project/httpapi_result.html",{"project": project, "object": httpresult })

@csrf_exempt
@login_required
def httpapi_delete(request, project_id, httpapi_id):
    project = Project.objects.get(id=project_id)
    httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
    if request.method == "GET":
        return  render(request, "project/httpapi_delete.html", {"project": project, "object": httpapi})
    
    if request.method == "POST":
        httpapi.delete()
        #return HttpResponse("delete ok")
        return redirect("httpapi_list",project.id)

@login_required
def test_create(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "GET":
        httpapis = project.httpapi_set.all()
        return  render(request, "project/httpapi_test_form.html", {"project": project, "objects": httpapis})
    if request.method == "POST":
        httprunresults = []
        httpapi_name = request.POST.get("httpapi_name")
        to = request.POST.getlist("to")
        httpapis = ",".join(to)
        httptest = HttpTest(name=httpapi_name,httpapis=httpapis,project=project)
        httptest.save()
        #return HttpResponse(httpapis)
        return redirect("test_list",project.id)

@login_required
def test_list(request, project_id):
    project = Project.objects.get(id=project_id)
    rs = HttpTest.objects.filter(project_id=project_id).order_by("-id")
    paginator = Paginator(rs, 5)
    page = request.GET.get('page')
    tests = paginator.get_page(page)
    return render(request,"project/test_list.html", {"project": project, "objects": tests})
    
@login_required
def test_run(request, project_id, test_id):
    project = Project.objects.get(id=project_id)
    test = HttpTest.objects.get(id=test_id)
    if request.method == "GET":
        httprunresults = []
        httprunresult_asserts = []
        httpapis = test.httpapis.split(",")
        for httpapi_id in httpapis:
            httpapi = HttpApi.objects.get(id=int(httpapi_id))
            httprunresult = utils.test_run(httpapi)
            httprunresults.append(str(httprunresult.id))
            httprunresult_asserts.append(httprunresult.assertResult)
        if "failed"  in httprunresult_asserts:
            status = "failed"
        else:
            status = "ok"
        httprunresults = ','.join(httprunresults)
        httptestresult = HttpTestResult(httptest=test, httprunresults=httprunresults,status=status)
        httptestresult.save()
        #return HttpResponse(httprunresults)
        return redirect("test_result",project_id, test_id)

@login_required            
def test_result(request, project_id, test_id):
    project = Project.objects.get(id=project_id)
    try:
        testresult = HttpTestResult.objects.filter(httptest_id=test_id).order_by("-id")[0]
    except:
        return render(request,"project/test_result.html", {"project":project})
    status = testresult.status
    httprunresult_ids = testresult.httprunresults.split(",")
    httprunresults = []
    ok_count = 0
    failed_count = 0
    for httprunresult_id in httprunresult_ids :
        httprunresult = HttpRunResult.objects.get(id=httprunresult_id)
        httprunresults.append(httprunresult)
        if httprunresult.assertResult == "ok":
            ok_count += 1
        if httprunresult.assertResult == "failed":
            failed_count += 1

    return render(request,"project/test_result.html", {"project":project, "testresult":testresult, "objects": httprunresults, "ok": ok_count,"failed": failed_count })


@login_required
def report_list(request, project_id):
    project = Project.objects.get(id=project_id)
    try:
        testresult = HttpTestResult.objects.filter(httptest__project=project).order_by("-id")
    except Exception as e:
        return render(request,"project/report_list.html", {"project":project})
    
    return render(request,"project/report_list.html", {"project":project,  "objects": testresult })


