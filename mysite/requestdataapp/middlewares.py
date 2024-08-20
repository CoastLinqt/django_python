import time
from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")

        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)

        print("after get response")

        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print(f"self.request_count = {self.request_count}")
        response = self.get_response(request)
        self.response_count += 1
        print(f"self.response_count = {self.response_count}")

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_time = {}

    def __call__(self, request: HttpRequest):
        delay = 1
        print(self.request_time)
        if not self.request_time:
            self.request_time['ip_address'] = request.META.get('REMOTE_ADDR')
            print(self.request_time)

        else:
            if ((round(time.time()) * 1) - self.request_time['time'] < delay and
                    self.request_time['ip_address'] == request.META.get('REMOTE_ADDR')):

                return render(request, "requestdataapp/request-errors_ratelimit.html")

        self.request_time.update({'time': round(time.time()) * 1})

        response = self.get_response(request)

        return response

