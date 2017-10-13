'''
创建者：徐洋
创建时间：2017年7月31日21:58:45
功能简述：根据用户输入自动生成一个包含insert,update,delete的存储过程模板
版本：v1.0
修改记录：
修改原因：
修改人：
修改时间：
'''
import datetime
import cx_Oracle
import os
os.environ["NLS_LANG"] = ".zhs16gbk"
##模块1：采集用户数据
#创建者姓名
createUser=input("请输入存储过程创建者姓名\n>>> ")
#程序功能描述
functionDescribe=input("简要描述一下该存储过程实现功能\n>>> ")
#创建时间
createTime=str(datetime.date.today())
#存储过程名字
procedureName=input("请输入你的存储过程名称\n>>> ")
#存储过程参数个数
numP=input("请输入你存储过程需要参数的个数(输入大于等于0的数字)\n>>> ")
while True:
    if numP.isdigit():
        numP = int(numP)
        break #程序结束
    else:
        print("请输入合法的数字")
#数据库用户名，密码，地址，数据库名称
dbUsername=input("数据库用户名\n>>> ")
dbPassword=input("数据库密码\n>>> ")
ip=input("数据库地址\n>>> ")
dbName=input("数据库名称\n>>> ")
print("提示:一般一秒之内就能连接上，若长时间停留在本消息上就关掉，检查输入的数据库连接信息")
conn=cx_Oracle.connect('{_dbUsername}/{_dbPassword}@{_ip}/{_dbName}'.format(_dbUsername=dbUsername,_dbPassword=dbPassword,_ip=ip,_dbName=dbName),)
while True:
    print("数据库连接成功")
    confirmProcedureName = input("确认你的存储过程名称是:{_procedureName}吗？[y/n]\n>>> ".format(_procedureName=procedureName))
    if confirmProcedureName == 'n':
        procedureName = input("请重新输入你的存储过程名称\n>>> ")
    elif confirmProcedureName == 'y':
        #到这里说明存储过程的名字就已经确定下来了，接下来一步新建文本文件
        procedureFile=open("{_procedureName}.txt".format(_procedureName=procedureName),'w')
        #模板的第一句话：创建语句
        line_1=str("create or replace procedure {_procedureName}").format(_procedureName=procedureName)
        procedureFile.write(line_1)
        #写入参数
        #判断用户输入的数字
        if numP != 0:
            for i in range(numP):
                P=input("第{_i}个参数名称\n>>> ".format(_i=i+1))
                while True:
                    P_LX_BM = input("第{_i}个参数的数据类型:1:varchar2,2:number,3:date\n>>> ".format(_i=i+1))
                    if P_LX_BM.isdigit():
                        if int(P_LX_BM) > 3 :
                            print("目前只支持3种类型，输入1或2或3即可")
                            break
                        else:
                            dict_lx={'1':'varchar2','2':'number','3':'date'}
                            if i==0 and numP!=1:
                                P_W='('+P+'      '+dict_lx[P_LX_BM]+'\n'
                            elif i==numP-1 and numP!=1:
                                P_W=','+P+'      '+dict_lx[P_LX_BM]+')'
                            elif i>0 and i < numP-1 and numP!=1:
                                P_W=','+P+'      '+dict_lx[P_LX_BM]+'\n'
                            else:#只有一个参数的情况
                                P_W='('+P+'      '+dict_lx[P_LX_BM]+')'
                            ##写入到文本中
                            procedureFile.write(P_W)
                            break
                    else:
                        print("非法字符！只能输入数字")
                        break
        #模板第二“句”话：注释
        line_2='''
----/******************************************************************
----{_procedureName}
----程序描述： {_functionDescribe}
----编写人员： {_createUser}
----创建日期： {_createTime}
----修改人员：
----修改日期：
----修改原因：
----修改人员：
----修改日期：
----修改原因：
----代码版本：	V1.0
----公司名称：	SALIEN（北京时林）
----******************************************************************/
'''.format(_procedureName=procedureName,_functionDescribe=functionDescribe,_createUser=createUser,_createTime=createTime)
        procedureFile.writelines(line_2)
        #模板第三“句”话：is 和 begin
        is_begin = ['is\n','--以下是变量\n',' \n','begin\n']
        procedureFile.writelines(is_begin)
        while True:
            userChoice = input("选择以下DML语句: 1:插入,2:删除,3:更新\n>>> ")
            if userChoice.isdigit():
                userChoice = int(userChoice)
                if userChoice not in [1,2,3]:
                    print("只能输入数字1或2或3")
                else:
                    if userChoice == 1:#插入
                        insTableName = input("需要插入数据的表名称\n>>> ")
                        cur = conn.cursor()
                        cur.execute("SELECT t.COLUMN_NAME,t.COMMENTS FROM user_col_comments t where t.TABLE_NAME=upper('{_insTableName}')".format(_insTableName=insTableName))
                        # 获得SQL语句执行返回的结果集，是一个二维元组
                        columnNameAndComment = cur.fetchall()
                        columnNameAndComment = list(columnNameAndComment)
                        str1=''
                        for index, item in enumerate(columnNameAndComment):##由于可能要修改注释，所以转化成列表处理
                            if item[1]==None:#有的字段没有注释，这里需要处理一下
                                item=list(item)
                                item[1]=''
                                if index == len(columnNameAndComment) - 1:
                                    str0 = '  ' + item[0] + '      --' + str(index + 1) + item[1] + '\n'
                                    str1 = str1 + str0
                                else:
                                    str0 = '  ' + item[0] + ',' + '     --' + str(index + 1) + item[1] + '\n'
                                    str1 = str1 + str0
                            else:
                                if index == len(columnNameAndComment) - 1:
                                    str0 = '  ' + item[0] + '      --' + str(index + 1) + item[1] + '\n'
                                    str1 = str1 + str0
                                else:
                                    str0 = '  ' + item[0] + ',' + '     --' + str(index + 1) + item[1] + '\n'
                                    str1 = str1 + str0
                        insModule = str('  insert into {_insTableName}{_str1}  commit;'.format(_insTableName=insTableName+ '\n'+'('+ '\n', _str1=str1+ '\n'+');'+ '\n'))
                        procedureFile.writelines(insModule + '\n')
                        continueChoice = input("是否继续?[y/n]\n>>> ")
                        if continueChoice == 'n':
                            procedureFile.writelines('end;')
                            procedureFile.close()
                            cur.close()
                            conn.close()
                            exit()
                    elif userChoice == 2:#删除
                        delTableName=input("需要删除数据的表名称\n>>> ")
                        delWhere=input("where条件是\n>>> ")
                        delModule=str('  Delete from {_delTableName}  where {_delWhere}  commit;').format(_delTableName=delTableName,_delWhere=delWhere+';'+'\n')
                        procedureFile.writelines(delModule+'\n')
                        continueChoice=input("是否继续?[y/n]\n>>> ")
                        if continueChoice=='n':
                            procedureFile.writelines('end;')
                            procedureFile.close()
                            exit()
                    elif userChoice == 3:#更新
                        updTableName = input("需要更新数据的表名称\n>>> ")
                        updWhere = input("where条件是\n>>> ")
                        cur=conn.cursor()
                        #执行SQL语句，获得表的列名和列的注释
                        cur.execute("SELECT t.COLUMN_NAME,t.COMMENTS FROM user_col_comments t where t.TABLE_NAME=upper('{_updTableName}')".format(_updTableName=updTableName))
                        #获得SQL语句执行返回的结果集，是一个二维元组
                        columnNameAndComment=cur.fetchall()
                        columnNameAndComment=list(columnNameAndComment)
                        #拼接SQL语句之字段部分
                        str1 = ''
                        for index, item in enumerate(columnNameAndComment):##由于可能要修改注释，所以转化成列表处理
                            if item[1]==None:#有的字段没有注释，这里需要处理一下
                                item=list(item)
                                item[1]=''
                                if index == len(columnNameAndComment) - 1:
                                    str0 = '                    ' + item[0] + '=' + '(此处自己填写相应字段名称)' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                                elif index not in (0, len(columnNameAndComment) - 1):
                                    str0 = '                    ' + item[0] + '=' + '(此处自己填写相应字段名称),' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                                else:
                                    str0 = item[0] + '=' + '(此处自己填写相应字段名称),' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                            else:
                                if index == len(columnNameAndComment) - 1:
                                    str0 = '                    ' + item[0] + '=' + '(此处自己填写相应字段名称)' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                                elif index not in (0, len(columnNameAndComment) - 1):
                                    str0 = '                    ' + item[0] + '=' + '(此处自己填写相应字段名称),' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                                else:
                                    str0 = item[0] + '=' + '(此处自己填写相应字段名称),' + '     --' + item[1] + '\n'
                                    str1 = str1 + str0
                        # 拼接SQL语句
                        updModule=str('  Update {_updTableName} set {_str1}  where {_updWhere}  commit;'.format(_updTableName=updTableName,_str1=str1,_updWhere=updWhere+';'+'\n'))
                        procedureFile.writelines(updModule + '\n')
                        continueChoice = input("是否继续?[y/n]\n>>> ")
                        if continueChoice == 'n':
                            procedureFile.writelines('end;')
                            procedureFile.close()
                            cur.close()
                            conn.close()
                            exit()
            else:
                print("只能输入数字1或2或3")

    else:
        print("只需要输入字母 y 或者 n即可")

