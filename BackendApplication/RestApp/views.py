from django.shortcuts import render
from RestApp.models import TaskModel
from rest_framework.views import APIView
from RestApp.serializers import TaskModelSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from RestApp.permissions import IsOwnerRole

#view for user registration
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

#view for user login
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

class TaskModelCompletedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tasks = TaskModel.objects.filter(completed = True)
        serializer = TaskModelSerializer(tasks, many = True)
        return Response(serializer.data)

#view for rest api's for task model
class TaskModelView(APIView):
    authentication_classes = [JWTAuthentication]

    #different rest api permissions methods for different user roles 
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsOwnerRole()]
        return [IsAuthenticated()]

    #handles get request
    def get(self, request, pk = None):
        #checking if we need to return result of particular task
        if(pk is not None):
            try:
                tasks = TaskModel.objects.get(id=pk)
            except:
                tasks = None 
                return Response(status = status.HTTP_204_NO_CONTENT)
            serializer = TaskModelSerializer(tasks)
        else: #it will return all objects result
            tasks = TaskModel.objects.all()
            if(len(tasks) == 0):
                return Response(status = status.HTTP_204_NO_CONTENT)
            serializer = TaskModelSerializer(tasks, many = True)
        return Response(serializer.data)

    #handles delete request
    def delete(self, request, pk):
        try:
            task = TaskModel.objects.get(id=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TaskModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    #handles post request
    def post(self, request):
        serializer = TaskModelSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)

    #handles put request
    def put(self, request, pk):
        try:
            task = TaskModel.objects.get(id=pk)
            serializer = TaskModelSerializer(task, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(status = status.HTTP_204_NO_CONTENT)
