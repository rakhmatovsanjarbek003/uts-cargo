from rest_framework import serializers
from .models import Cargo

class CargoTrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['track_code', 'status']