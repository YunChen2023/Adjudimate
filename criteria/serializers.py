from rest_framework import serializers
from .models import Criterion

class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterion
        fields = '__all__'