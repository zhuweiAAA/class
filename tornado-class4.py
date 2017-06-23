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


class ReverseHandler(tornado.web.RequestHandler):
    def get(self,input):
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width',40)
        self.write(textwrap.fill(text,int(width)))
    
"""
在同一个处理函数中定义多个方法是可能的，并且是有用的。把概念相关的功能绑定到
同一个类是一个很好的方法。比如，你可能会编写一个处理函数来处理数据库中某个特定
ID的对象，既使用GET方法，也使用POST方法。想象GET方法来返回这个部件的信息，
而POST方法在数据库中对这个ID的部件进行改变：

# matched with (r"/widget/(\d+)", WidgetHandler)
class WidgetHandler(tornado.web.RequestHandler):
    def get(self, widget_id):
        widget = retrieve_from_db(widget_id)
        self.write(widget.serialize())

    def post(self, widget_id):
        widget = retrieve_from_db(widget_id)
        widget['foo'] = self.get_argument('foo')
        save_to_db(widget)
"""

"""
我们到目前为止只是用了GET和POST方法，但Tornado支持任何合法的HTTP请求
（GET、POST、PUT、DELETE、HEAD、OPTIONS）。
你可以非常容易地定义上述任一种方法的行为，
只需要在RequestHandler类中使用同名的方法。下面是另一个想象的例子，
在这个例子中针对特定frob ID的HEAD请求只根据frob是否存在给出信息，
而GET方法返回整个对象：

# matched with (r"/frob/(\d+)", FrobHandler)
class FrobHandler(tornado.web.RequestHandler):
    def head(self, frob_id):
        frob = retrieve_from_db(frob_id)
        if frob is not None:
            self.set_status(200)
        else:
            self.set_status(404)
    def get(self, frob_id):
        frob = retrieve_from_db(frob_id)
        self.write(frob.serialize())
"""



if __name__=="__main__":

    tornado.options.parse_command_line()

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
    
