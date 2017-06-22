#-*-conding:utf-8-*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web



from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting','Hello')
        self.write(greeting+',friendly user!')

"""
到/reverse/string的GET请求将会返回URL路径中指定字符串的反转形式。
$ curl http://localhost:8000/reverse/stressed
desserts

$ curl http://localhost:8000/reverse/slipup
pupils
正则表达式告诉Tornado匹配任何以字符串/reverse/开始并紧跟着一个或多个字母的路径。
括号的含义是让Tornado保存匹配括号里面表达式的字符串，并将其作为请求方法的一个参
数传递给RequestHandler类。
get方法有一个额外的参数input。这个参数将包含匹配处理函数正则表达式第一个括号里的
字符串。（如果正则表达式中有一系列额外的括号，匹配的字符串将被按照在正则表达式中
出现的顺序作为额外的参数传递进来。）
"""
class ReverseHandler(tornado.web.RequestHandler):
    def get(self,input):
        self.write(input[::-1])

"""
这个处理函数定义了一个post方法，也就是说它接收HTTP的POST方法的请求。
我们之前使用RequestHandler对象的get_argument方法来捕获请求查询字符串的的参数。
同样，我们也可以使用相同的方法来获得POST请求传递的参数。（Tornado可以解析
URLencoded和multipart结构的POST请求）。一旦我们从POST中获得了文本和宽度的参数，
我们使用Python内建的textwrap模块来以指定的宽度装饰文本，并将结果字符串写回到
HTTP响应中。
"""
class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width',40)
        self.write(textwrap.fill(text,int(width)))
    

if __name__=="__main__":

    tornado.options.parse_command_line()

    """
    tornado在元组中使用正则表达式来匹配HTTP请求的路径。（这个路径是URL中主机名
    后面的部分，不包括查询字符串和碎片。）Tornado把这些正则表达式看作已经包含了
    行开始和结束锚点（即，字符串"/"被看作为"^/$"）。如果一个正则表达式包含一个
    捕获分组（即，正则表达式中的部分被括号括起来），匹配的内容将作为相应HTTP请
    求的参数传到RequestHandler对象中。
    """
    app = tornado.web.Application(
        handlers=[
            (r"/",IndexHandler),
            (r"/reverse/(\w+)",ReverseHandler),
            (r"/wrap",WrapHandler),
        ]
    )
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
