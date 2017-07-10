"""
Twitter时间轴
"""

import tornado.web
import tornado.httpserver
import tornado.auth
import tornado.ioloop
"""
TwitterHandler类包含我们应用逻辑的主要部分
这个类继承自能给我们提供Twitter功能的tornado.auth.TwitterMixin类，
其二是get方法使用了我们在第五章中讨论的@tornado.web.asynchronous装饰器。

"""
class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        oAuthToken = self.get_secure_cookie('oauth_token')
        oAuthSecret = self.get_secure_cookie('oauth_secret')
        userID = self.get_secure_cookie('user_id')

        """
        当一个用户请求我们应用的根目录时，我们首先检查请求是否包括一个oauth_token查询
        字符串参数。如果有，我们把这个请求看作是一个来自Twitter验证过程的回调
        """
        if self.get_argument('oauth_token', None):
           """
           使用auth模块的get_authenticated方法把给我们的临时令牌换为用户的访问令牌。这个方法
           期待一个回调函数作为参数，在这里是self._teitter_on_auth方法
           """
            self.get_authenticated_user(self.async_callback(self._twitter_on_auth))
            return
        #如果oauth_token参数没有被发现，我们继续测试是否之前已经看到过这个特定用户了
        elif oAuthToken and oAuthSecret:
            """
            寻找我们应用在Twitter给定一个合法用户时设置的access_key和access_secret cookies。
            如何这个值被设置了，我们就用key和secret组装访问令牌，然后使用self.twitter_request
            方法来向Twitter API的/users/show发出请求
            """
            accessToken = {
                'key': oAuthToken,
                'secret': oAuthSecret
            }
            """
            twitter_quest方法期待一个路径地址作为它的第一个参数，另外还有一些可选的关键字参数，
            如access_token、post_args和callback。access_token参数应该是一个字典，包括用户OAuth
            访问令牌的key键，和用户OAuth secret的secret键。如果API调用使用了POST方法，请求参数
            需要绑定一个传递post_args参数的字典。查询字符串参数在方法调用时只需指定为一个额外的
            关键字参数。在/users/show API调用时，我们使用了HTTP GET请求，所以这里不需要post_arg
            s参数，而所需的user_id API参数被作为关键字参数传递进来。
            """
            self.twitter_request('/users/show',
                access_token=accessToken,
                user_id=userID,
                callback=self.async_callback(self._twitter_on_user)
            )
            return
        """
        如果上面我们讨论的情况都没有发生，这说明用户是首次访问我们的应用（或者已经注销或删除
        了cookies），此时我们想将其重定向到Twitter的验证页面。调用self.authorize_redirect()
        来完成这项工作
        """
        self.authorize_redirect()

    """
    Twitter请求的回调方法非常的直接。_twitter_on_auth使用一个user参数进行调用，这个参数是已授权
    用户的用户数据字典。我们的方法实现只需要验证我们接收到的用户是否合法，并设置应有的cookies。
    一旦cookies被设置好，我们将用户重定向到根目录，即我们之前谈论的发起请求到/users/show API方
    法。
    """
    def _twitter_on_auth(self, user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500, 'Twitter authentication failed')

        self.set_secure_cookie('user_id', str(user['id']))
        self.set_secure_cookie('oauth_token', user['access_token']['key'])
        self.set_secure_cookie('oauth_secret', user['access_token']['secret'])

        self.redirect('/')

    """
    _twitter_on_user方法是我们在twitter_request方法中指定调用的回调函数。当Twitter响应用户的个人
    信息时，我们的回调函数使用响应的数据渲染home.html模板。这个模板展示了用户的个人图像、用户名
    、详细信息、一些关注和粉丝的统计信息以及用户最新的状态更新
    """
    def _twitter_on_user(self, user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

        self.render('home.html', user=user)

"""
LogoutHandler方法只是清除了我们为应用用户存储的cookies。它渲染了logout.html模板，来给用户提供反
馈，并跳转到Twitter验证页面允许其重新登录
"""
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.render('logout.html')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', TwitterHandler),
            (r'/logout', LogoutHandler)
        ]

"""
设置字典
"""
        settings = {
            'twitter_consumer_key': 'cWc3 ... d3yg',
            'twitter_consumer_secret': 'nEoT ... cCXB4',
            'cookie_secret': 'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==',
            'template_path': 'templates',
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
