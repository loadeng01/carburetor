from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import send_confirmation_email, send_activation_sms
from apps.car.permissions import IsAdminOrEmployee
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_activation_sms.delay(user.phone_number, user.activation_phone_code)
            except:
                return Response({'message': 'Registered, but trouble with phone number',
                                 'data': serializer.data}, status=201)
            try:
                send_confirmation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but trouble with email',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class RegisterEmployeeView(APIView):
    permission_classes = permissions.IsAdminUser,

    def post(self, request):
        serializer = RegisterEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class ActivationEmailView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activate', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )


class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_phone_code')
        user = User.objects.filter(phone_number=phone, activation_phone_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_phone_code = ''
        user.is_phone_active = True
        user.save()
        return Response('Successfully activated', status=200)


class Pagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class UserViewSet(ModelViewSet):
    permission_classes = IsAdminOrEmployee,
    queryset = User.objects.all()
    pagination_class = Pagination
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('email', )
    filterset_fields = ('is_staff', 'is_superuser', 'is_active', 'is_phone_active')









