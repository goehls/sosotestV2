from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.helper.ApiReturn import ApiReturn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json, traceback
from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.sourceService import SourceService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.helper.ApiReturn import ApiReturn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json, traceback
from apps.version_manage.services.common_service import VersionService
from all_models.models import *
from django.http import HttpResponseRedirect
from apps.common.model.RedisDBConfig import *
from apps.mock_server.services.mock_http_service import MockHttpService
from apps.common.func.ValidataFunc import *

from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.common.decorator.permission_normal_funcitons import *
from all_models_for_mock.models import *
from apps.common.func.ExecFunc import *

retmsg = ""
logger = logging.getLogger("django")


def http_interfaceCheck(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["mockinterfaceCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # ??????
    text = {}
    text["pageTitle"] = "MOCK????????????"
    context["text"] = text
    context["page"] = 1
    # context["lang"] = getLangTextDict(request)
    context["uri"] = UriService.getUri(request,"HTTP")

    addUserLog(request, "MOCK??????->??????MOCK->????????????->??????", "PASS")
    context["title"] = "HTTP MOCK"
    return render(request, "mock_server/http/HTTP_interface_check.html", context)

def http_interfaceListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "???????????????->????????????->????????????->?????????????????????", "FAIL")
        return HttpResponse("<script>alert('?????????????????????');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "???????????????->????????????->????????????->SQL???????????????????????????????????????", "FAIL")
        return HttpResponse("<script>alert('??????????????????');</script>")

    tbName = "tb4_mock_http"
    versionCondition = ""

    execSql = "SELECT i.*,u.userName,mu.userName modByName,b.bussinessLineName bussinessLineName,m.moduleName moduleName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id WHERE 1=1 and i.state=1 %s" % (
    tbName, versionCondition)
    print(execSql)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (i.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    print(checkList)
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum,request=request)
    context["host"] = request.get_host()
    for tmppagedata in context["pageDatas"]:
        followinfo = Tb4MockFollower.objects.filter(mockId=tmppagedata["mockId"], follower=request.session.get("loginName"), state=1).all()
        if followinfo:
            tmppagedata["followed"] = 1
        else:
            tmppagedata["followed"] = 0
    response = render(request, "mock_server/http/SubPages/HTTP_interface_list_check_page.html", context)
    addUserLog(request, "MOCK??????->??????HTTP MOCK->????????????->??????", "PASS")
    return response

@single_add_page_permission
def interfaceAddPage(request,context):
    interfaceAutoFillKey = "interfaceAutoFill_%s_%s" % (request.session.get("loginName"), int(time.time() * 1000))
    langDict = getLangTextDict(request)
    if request.GET.get("sendParam", None):
        params = request.GET.get("param", None)
        if params:
            RedisCache().set_data(interfaceAutoFillKey, params)
            RedisCache().expire_data(interfaceAutoFillKey, 60)
            context["interfaceAutoFillKey"] = interfaceAutoFillKey

    context["option"] = "add"
    context["mockaddHTTPInterface"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # ??????
    text = {}
    text["pageTitle"] = "??????MOCK??????"
    text["subPageTitle"] = "??????MOCK??????"
    context["text"] = text


    # ??????????????????
    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    # ????????????
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    addUserLog(request, "MOCK??????->??????MOCK->????????????->??????", "PASS")
    context["title"] = "??????HTTP MOCK"
    context["importStr"] = getPythonThirdLib()

    return render(request, "mock_server/http/HTTP_interface.html", context)

def interfaceGetSyncTestCaseStep(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        interfaceData = dbModelToDict(MockHttpService.getInterfaceForId(id))
        syncList = syncDelTipList(interfaceData)
    else:
        interfaceData = dbModelToDict(HTTP_interfaceService.getVersionInterfaceForId(id))
        syncList = syncVersionDelTipList(interfaceData, VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(body=syncList).toJson())

@single_data_permission(Tb4MockHttp,Tb4MockHttp)
def interfaceDel(request):
    id = request.GET.get("id")
    try:
        if VersionService.isCurrentVersion(request):
            interfaceData = MockHttpService.getInterfaceForId(request.GET.get("id"))
        else:
            interfaceData = MockHttpService.getVersionInterfaceForId(request.GET.get("id"))

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "??????id?????? %s" % e).toJson())

    if MockHttpService.delInterfaceForId(request,id) == 1:
        addUserLog(request, "MOCK??????->??????MOCK[%s]->?????????" % id, "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())

@single_page_permission
def operationInterface(request,context):
    langDict = getLangTextDict(request)
    context["id"] = request.GET.get("id")
    context["option"] = request.GET.get("option")
    context["addHTTPInterface"] = "current-page"
    context["title"] = "HTTP MOCK-"+request.GET.get("id")

    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["dataAddBy"] = MockHttpService.getInterfaceForId(request.GET.get("id")).addBy
        else:
            context["dataAddBy"] = MockHttpService.getVersionInterfaceForId(request.GET.get("id")).addBy

    except Exception as e:

        return render(request, "permission/page_404.html")

    # ??????
    text = {}
    try:
        text["pageTitle"] = "MOCK??????"
        if context["option"] == "select":
            text["subPageTitle"] = "??????MOCK??????"
        elif context["option"] == "edit":
            text["subPageTitle"] = "??????MOCK??????"
        elif context["option"] == "copy":
            text["subPageTitle"] = "??????MOCK??????"
    except Exception as e:
        return HttpResponse("???????????? %s" % e)
    context["text"] = text

    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    context["serviceJson"] = json.dumps(ServiceConfService.queryServiceConfSort(request))
    context["importStr"] = getPythonThirdLib()

    return render(request, "mock_server/http/HTTP_interface.html", context)

def getInterfaceDataForId(request):
    langDict = getLangTextDict(request)
    serviceConf = ServiceConfService.queryServiceConfSort(request)

    # ???????????????????????????????????????????????? ??????????????????20180224
    if VersionService.isCurrentVersion(request):
        getDBData = MockHttpService.getInterfaceForIdToDict(request.GET.get("id"))
        interfaceIdList = getDBData['interfaceIds'].strip(",").split(',')
        interfaceList = []
        for tmpInterfaceId in interfaceIdList:
            if tmpInterfaceId.strip() != "":
                interfaceList.append(dbModelToDict(HTTP_interfaceService.getInterfaceByInterfaceId(tmpInterfaceId.strip())))
        getDBData['interfaceList'] = interfaceList
    else:
        getDBData = MockHttpService.getVersionInterfaceForIdToDict(request.GET.get("id"),request.session.get("version"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], json.dumps(getDBData)).toJson())

def interfaceAdd(request):
    # ?????????????????????????????????????????????
    if request.method != 'POST':
        return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "??????????????????", "").toJson())
    data = json.loads(request.POST.get("interfaceData"))
    try:
        if 'advancedPythonCode' in data.keys():
            retB,retS = verifyPythonMode(data['advancedPythonCode'])
            if retB == False:
                retMsg = "????????????python???????????????%s" % retS
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, retMsg, retMsg).toJson())

        MockHttpService.addHttpMockInfo(data, request.session.get("loginName"))
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "??????????????????", "Failed: %s" % e).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "????????????", "").toJson())

@single_data_permission(Tb4MockHttp,Tb4MockHttp)
def interfaceSaveEdit(request):
    postLoad = json.loads(request.POST.get("interfaceData"))
    try:
        if 'advancedPythonCode' in postLoad.keys():
            retB,retS = verifyPythonMode(postLoad['advancedPythonCode'])
            if retB == False:
                retMsg = "????????????python???????????????%s" % retS
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, retMsg, retMsg).toJson())
        retm = MockHttpService.interfaceSaveEdit(request,postLoad)
        addUserLog(request, "MOCK??????->??????MOCK[%s]->?????????" % id, "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, message=retm).toJson())

    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '?????????????????????%s' % e).toJson())

def queryPeopleInterface(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    attrData = HTTP_interfaceService.queryPeopleInterface(pageNum, commonWebConfig.queryPeopleInterface,
                                                          request.session.get("loginName"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], attrData).toJson())

def updateInterfaceLevel(request):
    userToken = request.GET.get("token", "")

    if userToken == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="toekn??????").toJson())
    try:
        userData = TbUser.objects.get(token=userToken)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token???????????????????????????").toJson())

    interfaceId = request.GET.get("interfaceId", "")
    if interfaceId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="interfaceId???????????????").toJson())
    try:
        interfaceData = TbHttpInterface.objects.get(interfaceId=interfaceId, state=1)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="InterfaceId ????????????").toJson())

    if userData.loginName != interfaceData.addBy.loginName:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="???????????????????????????").toJson())

    levelDict = {"???": 0, "???": 5, "???": 9}
    levelText = request.GET.get("level", "???")

    if levelText in levelDict.keys():
        level = levelDict[levelText]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="level????????????????????????????????????????????????").toJson())

    interfaceData.caselevel = level
    interfaceData.save(force_update=True)
    return HttpResponse(ApiReturn().toJson())

def interfaceGetAutoFillData(request):
    interfaceAutoFillKey = request.GET.get("interfaceAutoFillKey", None)
    if interfaceAutoFillKey:
        try:
            sendParams = RedisCache().get_data(interfaceAutoFillKey)
            RedisCache().del_data(interfaceAutoFillKey)
        except Exception as e:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="???????????????????????????????????????").toJson())
        return HttpResponse(ApiReturn(body=sendParams).toJson())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="????????????KEY????????????????????????").toJson())

def getUrikeyByUrihost(request):
    host = request.GET.get("host", "")
    if host == "":
        return HttpResponse("")
    try:
        confHttp = TbConfigHttp.objects.filter(httpConf__contains=host)
        if confHttp:
            confHttp = confHttp[0]
            confDict = Config.getConfDictByString(confHttp.httpConf)
            for protocolKey, protocolValue in confDict.items():
                for uriKey, uriValue in protocolValue.items():
                    if uriValue == host:
                        return HttpResponse(uriKey)
            return HttpResponse("")
        else:
            return HttpResponse("")
    except:
        logging.error(traceback.format_exc())
        return HttpResponse("")

def runContrackTask(request):
    mockId = request.GET.get("mockId")
    httpConfKey = request.GET.get("httpConfKey")
    if(mockId):
        mockInfo = MockHttpService.getInterfaceByMockId(mockId)
        if mockInfo:
            if mockInfo.interfaceIds.strip(",").strip() == "":
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="?????????????????????????????????", body=mockId + httpConfKey).toJson())
        else:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="????????????mock?????????", body=mockId + httpConfKey).toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="?????????mockId?????????", body=mockId + httpConfKey).toJson())

    if httpConfKey:
        pass
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="?????????httpConfKey?????????", body=mockId + httpConfKey).toJson())

    taskExc = TbTaskExecute()
    taskExc.taskId = "CONTRACT_TASK_%s" % mockId
    taskExc.title = "???????????????%s" % mockInfo.title
    taskExc.taskdesc = taskExc.title
    taskExc.protocol = "HTTP"
    taskExc.businessLineGroup = "['%s']" % BusinessService.getBusinessLineNameById(mockInfo.businessLineId)
    taskExc.modulesGroup = "['%s']" % ModulesService.getModuleNameById(mockInfo.moduleId)
    taskExc.interfaceCount = len(mockInfo.interfaceIds.strip(",").split(","))
    taskExc.taskInterfaces = mockInfo.interfaceIds.strip(",")
    taskExc.caseCount = 0
    taskExc.interfaceNum = taskExc.interfaceCount

    taskExc.httpConfKey = TbConfigHttp.objects.filter(httpConfKey=httpConfKey.strip()).get()
    taskExc.execComments = "????????????????????????"
    taskExc.testResultMsg = ""
    taskExc.testReportUrl = ""

    taskExc.addBy = TbUser.objects.filter(loginName = request.session.get("loginName")).get()
    taskExc.execBy = TbUser.objects.filter(loginName = request.session.get("loginName")).get()
    taskExc.save(force_insert=True)

    addDataResult = dbModelToDict(taskExc)
    # ??????????????????????????????????????????????????????????????? taskExecute_executeId
    RedisCache().set_data("%s_taskExecute_%s" % ("HTTP", addDataResult["id"]), "0:0:0:0:0", 60 * 60 * 12)
    RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP", addDataResult["id"]), "1", 60 * 60 * 12)
    # tcpin = '{"do":3,"TaskExecuteId":"%s"}' % addDataResult["id"]
    tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP"}' % (addDataResult["id"], addDataResult["httpConfKey_id"], addDataResult["taskId"])
    retApiResult = send_tcp_request(tcpin)
    if retApiResult.code != ApiReturn.CODE_OK:
        retmsg = 1
        RedisCache().del_data("%s_taskExecute_%s" % ("HTTP", addDataResult["id"]))
        RedisCache().del_data("%s_taskExecuteStatus_%s" % ("HTTP", addDataResult["id"]))
    bodyDict = {
        "taskExecuteId":taskExc.id,
        "taskId":taskExc.taskId
    }
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="ok",body=bodyDict).toJson())

@catch_request_exception
def getContrackTaskRecentExecInfos(request):
    mockId = request.GET.get("mockId")
    taskId = "CONTRACT_TASK_%s" % mockId
    retList = executeSqlGetDict("select * from tb_task_execute where taskId='%s' order by addTime desc limit 0,10" % taskId)

    for pageData in retList:
        execProgressDataLen = pageData["execProgressData"].split(":")
        try:
            pageData["execPercent"] = "pass"
            pageData["execColor"] = "success"
            pageData["executeCount"] = (int(execProgressDataLen[1]) + int(execProgressDataLen[2]) + int(execProgressDataLen[3]))
            pageData["passCount"] = int(execProgressDataLen[1])
            pageData["failCount"] = int(execProgressDataLen[2])
            pageData["errorCount"] = int(execProgressDataLen[3])
            pageData["passPercent"] = int(
                (pageData["executeCount"] / int(execProgressDataLen[0])) * 100)

            if int(execProgressDataLen[2]) > 0 or int(execProgressDataLen[3]) > 0:
                pageData["execPercent"] = "fail"
                pageData["execColor"] = "danger"
        except ZeroDivisionError:
            pageData["passPercent"] = 0

        #?????????
        if pageData["version"] == "CurrentVersion":
            pageData["versionText"] = request.session.get("CurrentVersion")
        else:
            pageData["versionText"] = pageData["version"]
        #????????????
        if pageData["execComments"] == "":
            pageData["execComments"] = "-"

        #?????????????????????
        if pageData["isSaveHistory"] == 1:
            pageData["isSaveHistoryText"] = "???"
        else:
            pageData["isSaveHistoryText"] = "???"

        #??????????????????
        if str(pageData["isSendEmail"])[0] == "1":
            pageData["isSendEmailText"] = "???"
        else:
            pageData["isSendEmailText"] = "???"

    return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="ok",body=retList).toJson())

def follow(request):
    operate = request.GET.get("oprate", "follow")
    mockId = request.GET.get("mockId", "")
    follower = request.session.get("loginName")
    if mockId == "":
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="mockId??????").toJson())
    retcode, retmsg = MockHttpService.follow(mockId,operate,follower)
    return HttpResponse(ApiReturn(code=retcode,message=retmsg).toJson())
