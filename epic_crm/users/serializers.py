from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.filter(name__in=['Management', 'Sales', 'Support']),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        for group_name in groups_data:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        if password is not None:
            instance.set_password(password)

        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()

        if groups_data is not None:
            group_objects = [Group.objects.get(name=group_name) for group_name in groups_data]
            instance.groups.set(group_objects)

        return instance

    def validate_password(self, value):
        """
        Valide que le mot de passe est présent lors de la création.
        """
        if self.instance is None and not value:
            raise serializers.ValidationError("This field is required.")
        return value