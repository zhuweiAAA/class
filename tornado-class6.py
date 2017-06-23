#-*-conding:utf-8-*-



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

"""
这个Tornado应用定义了两个请求处理类：IndexHandler和MungedPageHandler。IndexHandler类简单地渲染了
index.html中的模板，其中包括一个允许用户POST一个源文本（在source域中）和一个替换文本（在change域中）
到/poem的表单。MungedPageHandler类用于处理到/poem的POST请求。当一个请求到达时，它对传入的数据进行一
些基本的处理，然后为浏览器渲染模板。map_by_first_letter方法将传入的文本（从source域）分割成单词，然
后创建一个字典，其中每个字母表中的字母对应文本中所有以其开头的单词（我们将其放入一个叫作source_map
的变量）。再把这个字典和用户在替代文本（表单的change域）中指定的内容一起传给模板文件munged.html。
此外，我们还将Python标准库的random.choice函数传入模板，这个函数以一个列表作为输入，返回列表中的任一
元素。在munged.html中，我们迭代替代文本中的每行，再迭代每行中的每个单词。如果当前单词的第一个字母是
source_map字典的一个键，我们使用random.choice函数从字典的值中随机选择一个单词并展示它。如果字典的键
中没有这个字母，我们展示源文本中的原始单词。每个单词包括一个span标签，其中的class属性指定这个单词是
替换后的（class="replaced"）还是原始的（class="unchanged"）。（我们还将原始单词放到了span标签的
title属性中，以便于用户在鼠标经过单词时可以查看是什么单词被替代了。
"""


import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                choice=random.choice)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "data\\class6\\templates"),
        static_path=os.path.join(os.path.dirname(__file__), "data\\class6\\static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    

"""
你可能注意到了debug=True的使用。它调用了一个便利的测试模式：tornado.autoreload模块，
此时，一旦主要的Python文件被修改，Tornado将会尝试重启服务器，并且在模板改变时会进行刷新。
对于快速改变和实时更新这非常棒，但不要再生产上使用它，因为它将防止Tornado缓存模板！
"""


