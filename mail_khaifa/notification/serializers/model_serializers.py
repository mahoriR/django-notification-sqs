from django.utils import timezone
from rest_framework import serializers

from ..models import AddrEntity

class AddrEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddrEntity
        fields = '__all__'
