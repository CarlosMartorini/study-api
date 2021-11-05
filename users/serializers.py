from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    # is_staff = serializers.BooleanField()
    # is_superuser = serializers.BooleanField()