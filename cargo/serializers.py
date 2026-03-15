from rest_framework import serializers
from .models import Cargo

class CargoTrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'track_code', 'status', 'created_at', 'delivered_at']