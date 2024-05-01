from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Todo
from .serializers import StudentSerializers, TodoSerializer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import json
import io

# Create your views here.

@api_view()
def home(request):
    print(request.query_params)
    # return HttpResponse(json.dumps(request.__dict__), content_type='application/json')
    # return JsonResponse({"name": "Dev", "age":22, "comment": "Meri umar ke naujawano!"})
    return Response({"name": "Dev", "age":22, "comment": "Meri umar ke naujawano!"})
    


# FBV to display all instances/records
@api_view(['GET'])
def all_todo(request):
    """
    Retrieve all todos.
    """
    all_todos = Todo.objects.all()
    todo_serializer = TodoSerializer(all_todos, many=True)
    return Response(todo_serializer.data, status=status.HTTP_200_OK)

# CBV to display all instances/records    
class AllTodos(GenericAPIView, ListModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# FBV to create a todo
@api_view(['POST'])
def add_todo(request):
    """
    Create a new todo.
    """
    todo_serializer = TodoSerializer(data = request.data)
    if todo_serializer.is_valid():
        todo_serializer.save()
        return Response(todo_serializer.data, status=status.HTTP_201_CREATED)
    return Response(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# CBV to create a todo    
class AddTodo(GenericAPIView, CreateModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# FBV to retrieve a single todo
@api_view(['GET'])        
def get_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({"error": "Todo does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    todo_serializer = TodoSerializer(todo)
    return Response(todo_serializer.data)

# CBV to retrieve a single todo
class GetTodo(GenericAPIView, RetrieveModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# CBV to update(full) a todo
class UpdateTodo(GenericAPIView, UpdateModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
# FBV to update(full/partial) a todo
@api_view(['PUT', 'PATCH'])
def update_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({"error": "Todo does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TodoSerializer(todo, data=request.data, partial=True)  # Set partial=True for PATCH
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FBV to delete a todo
@api_view(['DELETE'])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({"error": "Todo does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# CBV to delete a todo
class DeleteTodo(GenericAPIView, DestroyModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
    
    
    

@api_view()
def student_detail(request, pk=None):
    if pk is not None:
        student = Student.objects.get(id=pk)
        serializer = StudentSerializers(student)
    
        # Method 1
        # json_data = JSONRenderer().render(serializer.data)
        # return HttpResponse(json_data, content_type='application/json')

        # Method 2
        # return HttpResponse(json.dumps(serializer.data), content_type='application/json')
        
        # Method 3
        return JsonResponse(serializer.data)
    students = Student.objects.all()
    serializer = StudentSerializers(students, many=True)
    # Here, there's a twist. JsonResponse expects a disctionary. But students is a list of
    # dict objects. Hence, we have to switch off safe param.
    return Response(serializer.data)
# As we can see, Method 3 is more convenient, easy to remember, and optimised.


@csrf_exempt
def student_create(request):
    if request.method == 'POST':
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializers(data=python_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Data Created!"})
        return JsonResponse(serializer.errors)


