from OracleDB import OracleDBConnector
import cx_Oracle
from richp import RichTablePrinter
from rich.console import Console
import re
from mkdir import LogWriter


rtp = RichTablePrinter()

sql_servers={
    "账号/密码@主机地址:端口/Oracle服务名":"驱动路径"
}

#实例化输出对象
console = Console(record=True)

#实例化输出对象写入对象
log_writer = LogWriter()
        

#检查表空间使用情况
logsql1 = """
select f.tablespace_name,
       a.total,
       f.free,
       round((f.free / a.total) * 100) "% Free"
  from (select tablespace_name, sum(bytes / (1024 * 1024)) total
          from dba_data_files
         group by tablespace_name) a,
         (select tablespace_name, round(sum(bytes / (1024 * 1024))) free
            from dba_free_space
           group by tablespace_name) f
 WHERE a.tablespace_name = f.tablespace_name(+)
 order by "% Free"
"""
#检查数据库死锁
logsql2 = """
select sid,
       serial#,
       username,
       SCHEMANAME,
       osuser,
       MACHINE,     
       terminal,
       PROGRAM,
       owner,
       object_name,
       object_type,
       o.object_id
  from dba_objects o, v$locked_object l, v$session s
 where o.object_id = l.object_id
   and s.sid = l.session_id 
"""

sql_cmds={
    "select count(*) from v$session":{
        "检查说明":"当前数据库链接数:",
        "标题":("连接数:",),
    },

    "select status,database_status from v$instance":{
        "检查说明":"检查Oracle实列,数据库状态,分别必须为,OPEN和ACTIVE",
        "标题":("status","database_status"),
        0:['OPEN'],
        1:["3",'ACTIVE']
    },
    "select group#,status,type,member from v$logfile":{
        "检查说明":"检查Oracle在线日志状态,“STATUS”应该为非“INVALID”，非“DELETED”",
        "标题":("group#","status","type","member"),
        1:['None']
    },
        "select tablespace_name,status from dba_tablespaces":{
        "检查说明": "表空间状态,STATUS应该都为ONLINE",
        "标题": ("tablespace_name", "status"),
        1:["ONLINE"]
    },
    "select tablespace_name,status from dba_tablespaces":{
        "检查说明":"检查Oracle所有数据文件状态",
        "标题": ("name", "status"),
        1:["ONLINE"]
    },
    logsql2:{
        "检查说明":"查询目前锁对象信息",
        "标题": ("sid", " serial#", "username", "SCHEMANAME","osuser","MACHINE","terminal","PROGRAM","owner","object_name","object_type","object_id"),
    },
    logsql1:{
        "检查说明": "如果空闲率%Free小于10%以上(包含10%)，则注意要增加数据文件来扩展表空间而不要是用数据文件的自动扩展功能。”",
        "标题": ("tablespace_name", "total", "free", "Free%"),
    }
    
}

#将查询结果转换为字符串形式
def convert_to_str(data):
    return list(map(lambda x: str(x), data))

#将元组中指定下标的元组前添加"<>",并返回一个新的元组
def change(tmp :tuple,num :int):
    result = []
    for item,i in enumerate(tmp):
        if num == item and i != None:
            result.append("<>"+i)
            continue
        result.append(i)
    return tuple(result)

#如果元素不符合规范，则标记为以 '<>' 开头的红色字符串。
def mark_nonconforming_element(row, index, values):
    """
    如果元素不符合规范，则标记为以 '<>' 开头的红色字符串。

    Args:
        row (tuple): 元组表示的一行数据
        index (int): 要检查的索引
        values (list): 规范值的列表

    Returns:
        tuple: 标记后的行
    """
    return tuple(f"<>{element}" if idx == index and element not in values else element for idx, element in enumerate(row))

try:
    #迭代服务器列表
    for sql_server in sql_servers:
        # 创建 OracleDBConnector 实例
        db_connector = OracleDBConnector(sql_servers.get(sql_server),sql_server)
        console.log(sql_servers.get(sql_server),sql_server)
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",sql_server)[0]
        #输出巡检服务器IP地址
        console.print("巡检服务器服务器:",ip)
        #写入文本
        log_writer.create_folder_and_append_file(ip,console.export_html())
    #迭代数据库语句
        for sql_cmd in sql_cmds:
            #获取数据库详情
            informations = sql_cmds.get(sql_cmd)
            checking_information = informations.get("检查说明")
            #输出检查信息
            console.print(checking_information)
            #写入文本
            log_writer.create_folder_and_append_file(ip,console.export_html())
            title = informations.get("标题")
            #执行数据库语句
            rows = db_connector.execute_query_and_fetch_all(sql_cmd)
            #获取执行结果,并将结果转换为字符串类型
            result = [convert_to_str(x) for x in rows]

    #迭代数据库语句详情
            for information in informations:
                if isinstance(information,int):
                    for index, values in informations.items():

                        result = [mark_nonconforming_element(row, index, values) for row in result]


                    # for item,i in enumerate(result):
                    #     if i[information] not in value:
                    #         result[item] = change(result[item],information)
            
            rtp.print_table(ip,title,result)
except cx_Oracle.Error as error:
    print(f"Oracle Error: {error}")

finally:
    # 关闭数据库连接
    db_connector.close_connection()