from rest_framework import serializers
from child.models import Child
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class ChildSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = '__all__'  

    def get_age(self, obj):
        today = timezone.now().date()
        birth_date = obj.date_of_birth
        age = relativedelta(today, birth_date)
        return f"{age.years} years, {age.months} months"
    

    