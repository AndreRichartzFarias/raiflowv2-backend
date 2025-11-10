from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserSerializer

@ensure_csrf_cookie
@require_http_methods(["GET"])
def csrf_view(request):
    """Endpoint to ensure the CSRF cookie is set for the frontend."""
    return JsonResponse({"message": "CSRF cookie set"})

class CsrfView(APIView):
    permission_classes = [AllowAny]

    @ensure_csrf_cookie
    def get(self, request):
        return JsonResponse({'detail': 'CSRF cookie set'})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'Missing credentials'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        django_login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        django_logout(request)
        return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)

class MeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user