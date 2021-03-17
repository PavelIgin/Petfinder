from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

class LoginUser(viewsets.ViewSet):
    """
    класс для логирования пользователя
    """

    def login_user(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'status': 'successful login'})
            else:
                return Response({'status': 'account is disabled'})
        else:
            return Response({'status': 'invalid login'})
