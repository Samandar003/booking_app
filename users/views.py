from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import CustomUserModel
from .tokens import account_activation_token
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UserSerializer, UserRegisterSerializer
from django.db.transaction import atomic
from .authentication import CsrfExemptSessionAuthentication
from django.db import transaction
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .tokens import AccountActivationTokenGenerator, toke_gen_uniqe
from django.contrib.auth import get_user_model
User=get_user_model()

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data)

class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(data={'message': 'logout success'}, status=200)

class ActivateAccountView(APIView):
    def get(self, request, uid, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    permission_classes=(permissions.AllowAny,)
    
    @transaction.atomic
    def post(self, request):
        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.is_active=False
            user.save()
            token=toke_gen_uniqe()
            send_mail(
                subject='Activation link',
                message=None,
                html_message=f'Activation link: <a href="http://localhost:8000/users/verify/{token}">tap here</a>',
                from_email='samandarshoyimov04@gmail.com',
                recipient_list=[user.username],
                fail_silently=False, )
            token = Token(token=token, user=user)
            token.save()
            return Response({'detail': 'Email sent'}, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        token = request.GET.get('token')
        if token:
            try:
                token = Token.objects.get(token=token)
            except Token.DoesNotExist:
                return Response({'detail': 'Token not found'}, status=404)
            user = token.user
            user.is_active = True
            user.save()
            token.delete()
            return Response(data=UserSerializer(user).data, status=200)
        return Response({'detail': 'Token not found'}, status=404)


class SignUpView(APIView):
    # authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSessionView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)            
