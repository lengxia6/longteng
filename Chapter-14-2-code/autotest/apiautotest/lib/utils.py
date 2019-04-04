import  requests
from apiautotest.models import HttpApi, HttpRunResult
def test_run(httpapi):
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
    return httprunresult