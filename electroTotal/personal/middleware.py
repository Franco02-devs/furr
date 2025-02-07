from django.shortcuts import redirect

class CheckUserIsDeletedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.isDelete:
            return redirect('login')
        response = self.get_response(request)
        return response
