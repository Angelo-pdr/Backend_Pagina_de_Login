from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from core.models import CustomUser
from .serializers import UserSerializer, GroupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    if CustomUser.objects.filter(email=data['email']).exists():
        return Response({'E-mail já está em uso'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create_user(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password']
    )

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return Response({'Usuario cadastrado com sucesso'}, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key,
            }
            return Response({'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'Email ou senha invalido'}, status=status.HTTP_401_UNAUTHORIZED)
