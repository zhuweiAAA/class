#-*-conding:utf-8-*-


import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path


"""
Tornado通过extends和block语句支持模板继承，这就让你拥有了编写能够在合适的地方复用的流体模板的控制权和灵活性。
"""
"""
自动转义
Tornado会自动转义在双大括号间被渲染的表达式
autoescape=None
{% autoescape None %}
{{ mailLink }}
{% raw %}
linkify()和xsrf_form_html()函数
"""

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


"""
我们不再像之前那样通过使用一个处理类列表和一些其他关键字参数调用tornado.web.Application的构造函数来创建实例，
而是定义了我们自己的Application子类，在这里我们简单地称之为Application。在我们定义的__init__方法中，我们创建
了处理类列表以及一个设置的字典，然后在初始化子类的调用中传递这些值，就像下面的代码一样：
"""
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "data\class7\templates"),
            static_path=os.path.join(os.path.dirname(__file__), "data\class7\static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "Burt's Books | Home",
            header_text = "Welcome to Burt's Books!",
        )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

