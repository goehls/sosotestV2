FROM python:3.6.5 as python
#FROM ubuntu:latest
MAINTAINER boyi.zhang@shopee.com


COPY . /sosotest

WORKDIR /sosotest
RUN pip3 install -r install/require.txt
RUN chmod 777 start.sh
# 初始化
#set @@global.sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
#RUN python3 AutotestWebD/manage.py migrate
#RUN python3 AutotestWebD/apps/scripts/initial/A0000_init_myadmin_account.py
#RUN python3 AutotestWebD/apps/scripts/initial/A0000_init_myadmin_add_adminManagePermissionData.py
#RUN python3 AutotestWebD/apps/scripts/initial/A0000_init_tb_exec_python_attrs.py
#RUN python3 AutotestWebD/apps/scripts/initial/A0000_init_sources.py
#RUN python3 AutotestWebD/apps/scripts/initial/A0001_init_permission_data.py

EXPOSE 1211

CMD ["sh","start.sh"]

