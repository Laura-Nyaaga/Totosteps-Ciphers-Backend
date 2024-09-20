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
    

    
from autism_results.models import Autism_Results
from autism_image.models import Autism_Image

class AutismResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autism_Results
        fields = "__all__"
        

class AutismImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autism_Image
        fields = "__all__"        

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
    

    

