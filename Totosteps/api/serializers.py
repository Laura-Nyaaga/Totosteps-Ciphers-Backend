from rest_framework import serializers
from assessment.models import Assessment
from autism_results.models import Autism_Results
from autism_image.models import Autism_Image
from milestones.models import Milestone
from resources.models import Resource
from result.models import Result

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
 

# MILESTONE MODEL
class MilestoneSerializer(serializers.ModelSerializer):
     class Meta:
        model = Milestone
        fields = '__all__'

# ASSESSMENT MODEL
class AssessmentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Assessment
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def create(self, validated_data):
        milestone = validated_data.pop('milestone')
        answers = validated_data.pop('answers')
        parent_email = validated_data.pop('parent_email')

        # Create the Result object and save parent_email
        result = Result.objects.create(
            milestone=milestone,
            answers=answers,
            parent_email=parent_email
        )

        return result

#RESOURCE MODEL
class ResourceSerializer(serializers.ModelSerializer):
     class Meta:
        model = Resource
        fields = '__all__'