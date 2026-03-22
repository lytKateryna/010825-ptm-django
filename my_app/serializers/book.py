from rest_framework import serializers

from my_app.models import Book


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'published_date',
            'price',
            'discounted_price',
            'category',
            'is_bestseller'
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "published_date",
            "category",
            "genre",
            "is_bestseller",
            "pages",
            "publisher",
            "author",
        ]


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
