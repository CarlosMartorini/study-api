from rest_framework import serializers
from users.serializers import UsersSerializer


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    users = UsersSerializer(many=True)