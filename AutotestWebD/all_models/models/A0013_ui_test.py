# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from all_models.models.A0001_user import *
from all_models.models.A0002_config import *
from all_models.models.A0003_attribute import *
from all_models.models.A0006_testcase import *
import django.utils.timezone
import datetime

class TbUiTaskSimple(models.Model):
    taskId = models.CharField(db_column='taskId', unique=True, default="", max_length=25, verbose_name="任务ID")
    title = models.CharField(max_length=100, verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000, verbose_name="任务描述")
    businessLineId = models.IntegerField(db_column='businessLineId', default=1, verbose_name="businessLineId")
    moduleId = models.IntegerField(db_column='moduleId', default=1, verbose_name="模块Id")
    sourceGroup = models.CharField(db_column='sourceGroup', default="['电脑Web']", max_length=1000, verbose_name="任务包含的来源名称，例如 IOS 安卓 Web端 所有")
    tasklevel = models.IntegerField(default=5, verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    emailList = models.CharField(db_column='emailList', max_length=2000, default='', verbose_name="发送邮件列表，除却执行人execBy以外的其他收件人")  # release2 新增

    status = models.IntegerField(default=2, verbose_name="状态，1新建待审核 2审核通过 3审核未通过")
    # 基本信息
    fileName = models.CharField(max_length=300, db_column="fileName", verbose_name="文件名称")
    sheetName = models.CharField(max_length=300, db_column='sheetName', default="", verbose_name="执行的表单")
    fileAddBy = models.CharField(max_length=100, db_column="fileAddBy", verbose_name="文件添加人")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbUiTaskSimpleAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_task_simple'

class TbUITestExecute(models.Model):
    taskId = models.CharField(db_column='taskId', default="",max_length=25, verbose_name="任务ID")
    title = models.CharField(max_length=100,default="", verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000,default="", verbose_name="任务描述")
    businessLineId = models.IntegerField(db_column='businessLineId', default=1, verbose_name="businessLineId")
    moduleId = models.IntegerField(db_column='moduleId', default=1, verbose_name="模块Id")
    sourceGroup = models.CharField(db_column='sourceGroup', default="['电脑Web']", max_length=1000, verbose_name="任务包含的来源名称，例如 IOS 安卓 Web端 所有")
    tasklevel = models.IntegerField(default=5, verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")


    #基本信息
    fileName = models.CharField(max_length=300,db_column="fileName",verbose_name="文件名称")
    sheetName = models.CharField(max_length=300, db_column='sheetName', default="", verbose_name="执行的表单")
    fileAddBy = models.CharField(max_length=100,db_column="fileAddBy",verbose_name="文件添加人")

    #执行信息
    httpConfKey = models.CharField(max_length=300, db_column='httpConfKey',default="", verbose_name="执行环境的httpConfKey")
    reportDir = models.CharField(max_length=100,db_column="reportDir", verbose_name="测试报告路径")
    packageId = models.CharField(db_column='packageId', default="", max_length=25, verbose_name="包ID")
    serverId = models.IntegerField(db_column='serverId', default=0, verbose_name="执行本次的appium服务ia")

    #执行信息
    execStatus = models.IntegerField(db_column='execStatus', default=1, verbose_name="执行状态: NOTRUN = 1 RUNNING = 2 DONE = 3 EXCEPTION = 4 CANCELING = 10 CANCELED = 11")
    execCommand = models.CharField(max_length=5000,default="",db_column="execCommand",verbose_name="执行命令")
    execStartTime = models.DateTimeField(db_column='execStartTime',default="2018-02-01 00:00:00",verbose_name="执行开始时间")
    execEndTime = models.DateTimeField(db_column='execEndTime',default="2018-02-01 00:00:00",verbose_name="执行结束时间")
    execTakeTime = models.CharField(db_column='execTakeTime',default="0",max_length=100,verbose_name="执行使用时间")
    execProgressString = models.TextField(db_column="execProgressString",verbose_name="执行进度信息")

    execComments = models.CharField(db_column='execComments',default="", max_length=400,verbose_name="执行备注信息")
    isSendEmail = models.IntegerField(db_column='isSendEmail',default=0,verbose_name="是否发送邮件[是否发送:是否带附件:PASS是否发送:FAIL是否发送:ERROR是否发送:EXCEPTION是否发送]0的时候不发送，1开头的时候依次往后判断即可后面没有的都是1，例如11标识发送带附件所有情况都发送10标识发送不带附件所有情况都发送100标识发送不带附件成功不发送其他情况发送")
    emailList = models.CharField(db_column='emailList', max_length=2000,default='',verbose_name="发送邮件列表，除却执行人execBy以外的其他收件人")#release2 新增


    #执行结果信息
    testResult = models.CharField(max_length=300,default="",db_column="testResult",verbose_name="测试结果")
    testResultMessage = models.TextField(default="",db_column="testResultMessage",verbose_name="测试结果详情")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_test_execute'


class TbUITestExcel(models.Model):
    fileName = models.CharField(max_length=300,db_column="fileName",verbose_name="文件名称")
    sheetNames = models.CharField(max_length=500,db_column="sheetNames",default="",verbose_name="文件包含的表单")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_ui_test_excel"
        unique_together = (('fileName', 'addBy'),)