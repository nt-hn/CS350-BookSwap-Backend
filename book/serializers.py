from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    picture = serializers.ImageField(allow_empty_file=False, use_url=True,required=False)