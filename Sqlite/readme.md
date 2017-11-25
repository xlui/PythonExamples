# 简单的列出了Python sqlite3 模块中常用的 API

1. `sqlite3.connect(database, timeout, other optional arguments)`  
打开一个 sqlite 数据库文件，如果文件不存在则新建一个。
当一个数据库被多个连接访问，且其中一个修改了数据库，此时 SQLite 数据库被锁定，直到事务提交。
timeout 参数表示连接等待锁定的持续时间，直到发生异常断开连接。timeout 参数默认是 5.0（5 秒）。

2. `connection.cursor()`  
创建一个 cursor

3. `cursor.execute(sql, optional parameters)`  
执行一句 sql 语句。 该 sql 语句可以被参数化，用 '?' 做占位符
例如：cursor.execute('insert into people values(?, ?)', (who, age))

4. `connection.execute(sql, optional parameter)`  
不使用 cursor 直接执行 sql 语句的快捷方式

5. `cursor.executemany(sql, sql_of_parameters)`  
对于 sql_of_parameters 中的所有参数或映射执行一个 sql 语句

6. `connection.executemany(sql, sql_of_parameters)`  
不使用 cursor 直接执行 sql 语句的快捷方式

7. `cursor.executescript(sql_script)`  
执行一个 sql 脚本。会首先执行 commit()，然后执行 sql 脚本。所有脚本中的 sql 语句应该用分号(;)分隔

8. `connection.execute(sql_script)`  
不使用 cursor 直接执行 sql 语句的快捷方式

9. `connection.total_changes()`  
返回自数据库连接打开以来被修改、插入或删除的数据库总行数。

10. `connection.commit()`  
提交当前事务。如果没有调用该方法，所有自上一次 commit() 之后对数据库的操作对于其他数据库连接是不可见的

11. `connection.rollback()`  
回滚到上一次 commit() 的状态

12. `connection.close()`  
关闭数据库连接。该函数不会主动调用 commit()，所以自上一次 commit() 以来，你对数据库所做的所有更改都会消失。

13. `cursor.fetchone()`  
返回查询结果集的下一行。返回一个单一的序列，当没有更多可用数据时，返回 None

14. `cursor.fetchmany([size=cursor.arraysize])`  
返回查询结果集的下一行组。返回一个列表，当没有更多可用行时，返回一个空列表。

15. `cursor.fetchall()`  
返回查询结果集的所有剩余的行。返回一个列表，当没有可用行时，返回一个空列表。
