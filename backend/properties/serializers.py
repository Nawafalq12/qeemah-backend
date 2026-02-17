from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "legal_document_type",
            "land_type",
            "district",
            "street_name",
            "total_area",
            "street_front_length_m",
            "has_neighboring_lands",
            "neighboring_north",
            "neighboring_south",
            "neighboring_east",
            "neighboring_west",
            "north_street_width",
            "south_street_width",
            "east_street_width",
            "west_street_width",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "created_at"]
