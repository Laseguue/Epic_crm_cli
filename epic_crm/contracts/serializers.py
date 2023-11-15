from rest_framework import serializers
from .models import Contract
from django.contrib.auth import get_user_model

User = get_user_model()

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('creation_date',)

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if user.groups.filter(name='Sales').exists():
            validated_data['sales_contact'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        if user.groups.filter(name='Sales').exists():
            validated_data.pop('sales_contact', None)
            validated_data.pop('client', None)

        status = validated_data.pop('status', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if status is not None:
            instance.status = status

        instance.save()
        return instance

