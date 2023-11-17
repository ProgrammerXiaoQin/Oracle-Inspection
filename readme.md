#### 准备事项

1. python 3.5以上版本

2. 用到的库 

   ```python
   pip install richp
   pip install cx_Oracle
   ```

3. 到Oracle官网下载cx_Oracle对应版本的驱动 , 并将驱动解压到程序目录
   - 可参考`https://oracle.github.io/odpi/doc/installation.html#linux`

#### 添加Oracle检查服务器地址

1. 打开Oracle.py , 里面有个字典`sql_servers` , key为服务器链接地址,value为Oracle对应版本驱动的path
   - 服务器链接地址格式`账号/密码@主机地址:端口/Oracle服务名`