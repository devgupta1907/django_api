from django.urls import path
from appri import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('get/', views.AllTodos.as_view(), name="get_all_todos"),
    # path('get/<int:pk>', views.get_todo, name="get_todo_detail"),
    path('create/', views.AddTodo.as_view(), name="create_todo"),
    path('update/<int:pk>', views.UpdateTodo.as_view(), name='update_todo'),
    path('get/<int:pk>', views.DeleteTodo.as_view(), name="delete_todo"),
]