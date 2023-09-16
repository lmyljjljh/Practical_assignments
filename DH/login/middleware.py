"""
中间件的作用：每次请求和响应都会调用
中间件的定义

中间件的使用：如果有多次需要判断或请求的我们可以使用中间件
"""
from django.http import HttpResponse
import time
from django.utils.deprecation import MiddlewareMixin

# ip池
ip_pool = {}
# def simple_middleware(get_response):
#     def middleware(request):
#         response = get_response(request)
#         # # 获取访问者IP
#         ip = request.META.get("REMOTE_ADDR")
#         # 获取访问当前时间
#         visit_time = time.time()
#         print(visit_time)
#         # 判断如果访问IP不在池中,就将访问的ip时间插入到对应ip的key值列表,如{"127.0.0.1":[时间1]}
#         if ip not in ip_pool:
#             ip_pool[ip] = [visit_time]
#             return response
#         # 然后在从池中取出时间列表
#         history_time = ip_pool.get(ip)
#         # 循环判断当前ip的时间列表，有值，并且当前时间减去列表的最后一个时间大于60s，把这种数据pop掉，这样列表中只有60s以内的访问时间，
#         while history_time and visit_time - history_time[-1] > 5:
#             history_time.pop()
#         # 如果访问次数小于4次就将访问的ip时间插入到对应ip的key值列表的第一位置,如{"127.0.0.1":[时间2,时间1]}
#         print(ip_pool)
#         print(history_time)
#         if len(history_time) < 4:
#             history_time.insert(0, visit_time)
#             return response
#         else:
#             # 如果大于3次就禁止访问
#             return HttpResponse("访问过于频繁,还需等待%s秒才能继续访问" % int(5 - (visit_time - history_time[-1])))
#     return middleware


from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print('request from {}'.format(request.META['REMOTE_ADDR']))
        print("中间件方法 process_request 被调用")


    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("中间件方法 process_view 被调用")

    def process_response(self, request, response):
        # print("中间件方法 process_response 被调用")
        # # 获取访问者IP
        ip = request.META.get("REMOTE_ADDR")
        # 获取访问当前时间
        visit_time = time.time()
        # print(visit_time)
        # 判断如果访问IP不在池中,就将访问的ip时间插入到对应ip的key值列表,如{"127.0.0.1":[时间1]}
        if ip not in ip_pool:
            ip_pool[ip] = [visit_time]
            return response
        # 然后在从池中取出时间列表
        history_time = ip_pool.get(ip)
        # 循环判断当前ip的时间列表，有值，并且当前时间减去列表的最后一个时间大于5s，把这种数据pop掉，这样列表中只有5s以内的访问时间，
        while history_time and visit_time - history_time[-1] > 5:
            history_time.pop()
        # 如果访问次数小于4次就将访问的ip时间插入到对应ip的key值列表的第一位置,如{"127.0.0.1":[时间2,时间1]}
        # print(ip_pool)
        # print(history_time)
        if len(history_time) < 4:
            history_time.insert(0, visit_time)
            return response
        else:
            # 如果大于3次就禁止访问
            return HttpResponse("访问过于频繁,还需等待%s秒才能继续访问" % int(5 - (visit_time - history_time[-1])))

        # return response

    def process_exception(self, request, exception):
        # print("中间件方法 process_exception 被调用")
        return HttpResponse('发生异常了')
