from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
    def validate_support_contact(self, value):
        if value is not None and not value.groups.filter(name='Support').exists():
            raise serializers.ValidationError("Seul un utilisateur du groupe Support peut être assigné en tant que support_contact.")
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()
        return instance