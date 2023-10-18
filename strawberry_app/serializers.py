from rest_framework import serializers
from strawberry_app.models import *


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = "__all__"


class MonthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = "__all__"
