from rest_framework import serializers
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