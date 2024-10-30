from datetime import date
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.serializers import SerializerMethodField
from assessment.models import Assessment
from autism_results.models import Autism_Results
from autism_image.models import Autism_Image
from milestones.models import Milestone
from resources.models import Resource
from result.models import Result
from users.models import User
from child.models import Child
from django.utils import timezone
from dateutil.relativedelta import relativedelta



# AUTISM RESULT MODEL
class AutismResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autism_Results
        fields = "__all__"

# AUTISM IMAGE MODEL    
class AutismImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autism_Image
        fields = "__all__"        
        



# CHILD MODEL
class ChildSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ['child_id', 'username', 'date_of_birth', 'is_active', 'parent', 'age']
        read_only_fields = ['child_id', 'is_active', 'age']

    def get_age(self, obj):
        today = timezone.now().date()
        birth_date = obj.date_of_birth
        age = relativedelta(today, birth_date)
        return f"Is {age.years} years, {age.months} months old"
    
    def validate_date_of_birth(self, value):
        today = date.today()
        age = relativedelta(today, value)
        
        if age.years > 3 or (age.years == 3 and age.months > 0):
            raise serializers.ValidationError("Only children below three years are allowed.")
        
        return value
 

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

# RESULT
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def create(self, validated_data):
        milestone = validated_data.pop('milestone')
        answers = validated_data.pop('answers')
        user = validated_data.pop('user')
        
        result = Result.objects.create(
            milestone=milestone,
            answers=answers,
            user=user
        )

        return result

#RESOURCE MODEL
class ResourceSerializer(serializers.ModelSerializer):
     class Meta:
        model = Resource
        fields = '__all__'

# USERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    


class ProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'permissions']

    def get_permissions(self, obj):
        permissions = obj.user_permissions.values_list('codename', flat=True)
        return list(permissions)
    
class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields ='__all__'
       
class ParentListSerializer(serializers.ModelSerializer):
    children = ChildListSerializer(many=True, read_only=True) 

    class Meta:
        model = User
        fields = '__all__'
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
            
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
            
        return data