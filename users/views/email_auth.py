from rest_framework import viewsets
from users.serializer import EmailAuthSerialazer
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models.email_auth_models import EmailAuthAsk


class EmailAuth(viewsets.ViewSet):

    @action(methods=['post'], detail=True, permission_classes=['IsAuthenticated'])
    def create(self, request):
        """
        При введении пароля пользователя и email отправляет сообщение на email
        """
        serializer = EmailAuthSerialazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['password'] != request.user.password:
            return Response({'status': 'неправильный пароль'})
        serializer.email_auth(validated_data=serializer.validated_data, request=request)
        return Response({'status': 'check your email'})

    @action(methods=['get'], detail=True, permission_classes=['AllowAny'])
    def get(self, request):
        """
        Принимает запрос и привязывает email при совпадении ключей
        """
        norm_key = EmailAuthAsk.objects.get(key=request.GET['key'])
        norm_key.user.email = norm_key.email_e
        norm_key.user.save(update_fields=['email'])
        return Response({'status': 'email is auth'})
