#-*-conding:utf-8-*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web



from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)


if __name__=="__main__":

    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r"/",IndexHandler),
            (r"/poem",PoemPageHandler)
        ],
        template_path = os.path.join(os.path.dirname(__file__),"data\\templates")
    )
    
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

"""
使用Python解释器导入模板模块尝试模板系统
from tornado.template import Template
content = Template("<html><body><h1>{{ header }}</h1></body></html>")
print content.generate(header="Welcome!")

填充表达式
>>> from tornado.template import Template
>>> print Template("{{ 1+1 }}").generate()
2
>>> print Template("{{ 'scrambled eggs'[-4:] }}").generate()
eggs
>>> print Template("{{ ', '.join([str(x*x) for x in range(10)]) }}").generate()
0, 1, 4, 9, 16, 25, 36, 49, 64, 81

填充Python变量的值到模板的双大括号中
将任何Python表达式放在双大括号中
在Tornado模板中使用Python条件和循环语句。控制语句以{%和%}包围
Tornado模板语言的一个最好的东西是在if和for语句块中可以使用的表达式没有限制。
也可以在你的控制语句块中间使用{% set foo = 'bar' %}来设置变量

在模板中使用函数
escape(s)
url_escape(s)
json_encode(val)
squeeze(s)

在模板中使用一个你自己编写的函数也是很简单的：只需要将函数名作为模板的参数传递即可，就像其他变量一样。

>>> from tornado.template import Template
>>> def disemvowel(s):
...     return ''.join([x for x in s if x not in 'aeiou'])
...
>>> disemvowel("george")
'grg'
>>> print Template("my name is {{d('mortimer')}}").generate(d=disemvowel)
my name is mrtmr

"""
    
