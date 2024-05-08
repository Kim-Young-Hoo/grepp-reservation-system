from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from project import config
from users.models import User
from users.serializers import UserSerializer
import jwt
import datetime


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDetailView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        token = request.COOKIES.get(config.JWT_COOKIE_KEY)
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, config.SECRET_KEY, config.HASH_ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = self.get_object(pk=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password')

        utcnow = datetime.datetime.utcnow()
        payload = {
            'id': user.id,
            'exp': utcnow + datetime.timedelta(minutes=60),
            'iat': utcnow
        }

        token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.HASH_ALGORITHM)

        response = Response()
        response.set_cookie(key=config.JWT_COOKIE_KEY, value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(config.JWT_COOKIE_KEY)
        response.data = {
            'message': 'success'
        }
        return response
