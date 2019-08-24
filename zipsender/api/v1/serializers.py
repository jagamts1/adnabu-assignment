from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    urls = serializers.ListField(child=serializers.URLField(
        max_length=200, min_length=None, allow_blank=False))
