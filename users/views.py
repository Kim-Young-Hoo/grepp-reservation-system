from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from project import config
from users.models import User
from users.serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user).key
        return Response({**serializer.data, "token": token})


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        token = Token.objects.get(user=user).key

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password')

        return Response({"token": token, "is_staff": user.is_staff})
