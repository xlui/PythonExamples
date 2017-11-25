# Flask-RESTful-API
使用 Python 的 Flask 框架实现使用了工厂模式的 RESTful 服务。

## 知识储备
1. HTTP 方法的含义与示例  

 HTTP方法 |   动作   |   示例   |  
---------|--------|---------|
GET|获取资源信息|http://example.com/api/resource
GET|获取资源信息|http://example.com/api/resource/123
POST|创建一个资源|http://example.com/api/resource
PUT|更新一个资源|http://example.com/api/resource/123
DELETE|删除一个资源|http://example.com/api/resource/123

2. API 返回的常见的 HTTP 状态码

HTTP状态码|消息|说明
---:|:---:|:---:
100|Continue|只有请求的一部分被服务器接收，但只要它没有拒绝，客户端应继续该请求
101|Switching Protocols|服务器切换协议
200|OK|请求成功完成
201|Created|请求成功地创建了一个新资源
202|Accepted|该请求被接受处理，但是该处理是不完整的
203|Non-authoritative Information|
204|No Content|
205|Reset Content|
206|Partial Content|
300|Multiple Choices|链接列表。用户可以选择一个链接，进入到该位置。最多五个地址
301|Move Permanently|所请求的页面已经转移到一个新的 URL
302|Found|所请求的页面已经临时转移到一个新的 URL
303|See Other|所请求的页面可以在另一个不同的 URL 下被找到
304|Not Modified|
305|Use Proxy|
306|Unused|在以前的版本中使用该代码。现在已经不再使用它，但代码仍被保留
307|Temporary Redirect|所请求的页面已经临时转移到一个新的 URL
400|Bad Request|服务器不理解请求
401|Unauthorized|请求未包含认证信息
402|Payment Required|您还不能使用该代码
403|Forbidden|禁止访问所请求的页面
404|Notfound|URL对应的资源不存在
405|Method not allowed|指定资源不支持请求使用的方法
406|Not Acceptable|服务器只生成一个不被客户端接收的响应
407|Proxy Authentication Required|在请求送达之前必须使用代理服务器的验证
408|Request Timeout|请求需要的时间比服务器能够等待的时间长，超时
410|Gone|所请求的页面不再可用
411|Length Required|"Content-Length" 未定义。服务器无法处理客户端发来的不带 Content-Length 的请求信息
412|Precondition Failed|请求中给出的先决条件被服务器评估为 false
413|Request Entity Too Large|服务器不接受该请求，因为请求实体过大
414|Request-url Too Long|服务器不接受该请求，因为 URL 太长
415|Unsupported Media Type|服务器不接收该请求，因为媒体类型不被支持
417|Expectation Failed|
500|Internal Server Error|未完成的请求。服务器遇到了一个意外的情况
501|Not Implemented|未完成的请求。服务器不支持所需的功能
502|Bad Gateway|未完成的请求。服务器从上游服务器收到无效响应
503|Service Unavailable|未完成的请求。服务器暂时超载或者死机
504|Gateway Timeout|网关超时
505|Http Version Not Supported|服务器不支持 "Http协议" 版本

## 使用方法(Usage)
首先进入 shell 环境为数据库添加默认数据
> python manage.py shell  
> db.drop_all()  
> db.create_all()  
> Tasks.init()  
> db.session.commit()  
> exit()

运行项目：
> python manage.py runserver

接下来开始验证：  
> GET(all tasks -- cannot access because of security authorization):  
> curl -i http://localhost:5000/api/v1.0/tasks  
> GET(all tasks -- use built-in username and password to access)  
> curl -i -u ok:python http://localhost:5000/api/v1.0/tasks
> 
> GET(single task):  
> curl -i http://localhost:5000/api/v1.0/tasks/1  
>
> POST:  
>curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/api/v1.0/tasks  
>
> PUT:  
>curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/api/v1.0/tasks/2  
>
> DELETE:  
>curl -i -X DELETE http://localhost:5000/api/v1.0/tasks/2  
