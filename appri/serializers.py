from rest_framework import serializers
from .models import Student, Todo

class StudentSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=50)

    def create(self, validate_data):
        return Student.objects.create(**validate_data)


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'completed', 'created_at', 'updated_at')