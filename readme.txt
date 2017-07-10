1. curl下载地址
https://curl.haxx.se/download.html

2.教程
http://shouce.jb51.net/tornado/ch1.html#ch1-2-1

3.测试工具
Siege utility 
例子： $ siege http://localhost:8000/?q=pants -c10 -t10s
http://shouce.jb51.net/tornado/ch2.html

4. 对于yield 的理解  在函数内执行到yield 语句时，就会向外输出一个结果（跳出函数）,当再次调用该函数时，从yield语句的下一句开始执行，同时上次函数运行过程中的本地变量值维持不变（不会重新初始）


5.
https://github.com/tornadoweb/tornado/wiki/Links

6.HTTP长轮询

7.Nginx 反向代理
8.Supervisor监控Tornado进程
