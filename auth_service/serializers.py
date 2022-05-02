import re

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "groups"
        ]

    def to_representation(self, instance):
        groups = []
        for i in instance.groups.all():
            groups.append(i.name)
        representation = {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'groups': groups
        }
        return representation

    def __check_username(self, username):
        try:
            return User.objects.get(username=username)
        except Exception:
            return False

    def __check_email(self, email):
        try:
            return User.objects.get(email=email)
        except Exception:
            return False

    def __check_password(self, password):
        if len(password) < 8:
            return 1
        elif not bool(re.search("[a-z]", password)):
            return 2
        elif not bool(re.search("[A-Z]", password)):
            return 3
        elif not bool(re.search(r'\d', password)):
            return 4

    def create(self, validated_data):
        if self.__check_username(validated_data["username"]):
            raise serializers.ValidationError("User with such username already exists!!!")
        elif self.__check_email(validated_data["email"]):
            raise serializers.ValidationError("User with such email already exists!!!")
        elif self.__check_password(validated_data["password"]) == 1:
            raise serializers.ValidationError("Password is too short!!!")
        elif self.__check_password(validated_data["password"]) == 2:
            raise serializers.ValidationError("Password must contain lowercase letters!!!")
        elif self.__check_password(validated_data["password"]) == 3:
            raise serializers.ValidationError("Password must contain uppercase letters!!!")
        elif self.__check_password(validated_data["password"]) == 4:
            raise serializers.ValidationError("Password must contain digits!!!")
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        user.save()
        for group_name in validated_data["groups"]:
            group = Group.objects.get(name=group_name)
            group.user_set.add(user)
        return user


class ChangeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            # "email",
            "groups"
        ]

    def to_representation(self, instance):
        groups = []
        for i in instance.groups.all():
            groups.append(i.name)
        representation = {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'groups': groups
        }
        return representation
