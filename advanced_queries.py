import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()


# ---------------------------------------------------------------------------------------------

# LOCAL IMPORTS

from django.db.models import (
    Count,
    Min,
    Max,
    Sum,
    Avg, QuerySet, ExpressionWrapper, F
)

from my_app.models import Book


# books_count = Book.objects.aggregate(
#     qwerty=Count('id'),
#     min_price=Min('price'),
#     max_price=Max('price')
# )
#
#
# print(type(books_count))
# print(books_count)
# print(books_count['qwerty'])


# author_books_count = Book.objects.values('author_id').annotate(
#     books_count=Count('id')
# )
#
# print(type(author_books_count))
# print(author_books_count)
#
# for book in author_books_count:
#     # print(book)
#     print(f"Author: {book['author_id']} | Books count: {book['books_count']}")



# Шпаргалка по values() !!!!! ВОЗВРАЩАЕТ СЛОВАРИК !!!!!


# QuerySet.values() --> --> из всех колонок возьми только те, что указаны в values
# QuerySet.values().annotate() --> --> проведи выполнение аггрегатной функции, сгруппируй всё по тем колонкам, которые указаны в values
# QuerySet.values().annotate().values() --> --> Сперва проведи группировку по values из всех колонок возьми только те, что указаны в values
# QuerySet.values().annotate().values().order_by()



# author_id, first_name, last_name, aggregation_column -> .values('author_id', 'aggregation_column') -> 'author_id', 'aggregation_column'


# all_books = Book.objects.all()
#
#
# print(all_books.query)
#
#
# # slised_books = Book.objects.all()[<start>:<stop>:<step>]
# slised_books = Book.objects.all()[10:20]
#
# print(slised_books.query)


# # получить книги, цена которых больше средней цены
# avg_book_price = Book.objects.aggregate(
#     avg_price=Avg('price')
# )['avg_price']
#
#
# books_with_price_gt_avg = Book.objects.filter(
#     price__gt=avg_book_price
# )
#
# print(books_with_price_gt_avg.query)
#
# for book in books_with_price_gt_avg:
#     print(f"Book price: {book.price}")


from django.db.models import Subquery

# получить книги, цена которых больше средней цены

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# avg_book_price = Book.objects.values().annotate(
#     avg_price=Avg('price')
# ).values('avg_price')[0]
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# print(avg_book_price.query)

# print(avg_book_price)
#
# for i in avg_book_price:
#     print(i)


# books_with_price_gt_avg = Book.objects.filter(
#     price__gt=Subquery(avg_book_price)
# )
#
# print(books_with_price_gt_avg.query)
#
# for book in books_with_price_gt_avg:
#     print(f"Book price: {book.price}")
#

# from django.db.models import OuterRef, Subquery
# # отобразить минимальную цену книги того же автора
#
# subquery = Book.objects.filter(
#     author=OuterRef('author')
# ).values('author').annotate(
#     min_book_price=Min('price')
# ).values('min_book_price')
#
# # print(subquery.query)
#
#
# main_query = Book.objects.filter(
#     published_date__lte="2015-12-31"
# ).annotate(
#     min_book_price=Subquery(subquery)
# )
#
# print(main_query.query)
#
# # SELECT *, () AS min_book_price
# # FROM books;
#
# for book in main_query:
#     print(f"{book.title=}  {book.author=}  {book.price=}  {book.min_book_price}")




# EXPRESSION WRAPPERS


# ExpressionWrapper(<expression>, <output_field>)

# добавить +1 колонку (цена за одну страницу книги)

# data = Book.objects.annotate(
#     price_per_page=(F('price') / F('pages')) * 0.13
# )
#
# print(data.query)
#
#
# for book in data[:3]:
#     print(f"Book: {book.title}")
#     print(f"Price: {book.price}")
#     print(f"Pages: {book.pages}")
#     print(f"Price per page: {book.price_per_page}")


# from django.db.models import DecimalField
#
# data = Book.objects.annotate(
#     price_per_page=ExpressionWrapper(
#         (F('price') / F('pages')) * 0.13,
#         output_field=DecimalField(
#             max_digits=6,
#             decimal_places=2
#         )
#     )
# )
#
# print(data.query)
#
#
# for book in data[:3]:
#     per_page = round(book.price_per_page, 4) if book.price_per_page else None
#     print(f"Book: {book.title}")
#     print(f"Price: {book.price}")
#     print(f"Pages: {book.pages}")
#     print(f"Price per page: {per_page}")
#     print(f"Price per page: {type(per_page)}")



# from rest_framework import serializers
#
#
# class MyTestSerializer(serializers.Serializer):
#     engine_type = serializers.CharField(
#         required=True,
#         max_length=10
#     )
#     color = serializers.CharField(
#         required=True,
#         max_length=15
#     )
#     type = serializers.CharField(
#         required=False,
#         max_length=10
#     )
#     year = serializers.DateField(
#         required=False
#     )
#
#
# data = {
#     # "engine_type": "VT-975",
#     "color": "black",
#     "type": "vehicle",
#     "year": "2001-04-20",
# }
#
# serializer = MyTestSerializer(data=data)
#
# print(serializer)
# print(serializer.validated_data)

# from rest_framework.exceptions import ValidationError
#
# try:
#     serializer.is_valid(raise_exception=True)
#     print(serializer.validated_data)
#
# except ValidationError as exc:
#     print(exc)

# if serializer.is_valid():
#     print(serializer.validated_data)
# else:
#     print(serializer.errors)

# False.validated_data



from rest_framework import serializers
from my_app.models import Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ['id', 'name'] # если нужны конкретные поля -- берём список
        fields = '__all__' # если нужны ВСЕ поля -- берём строку


categories = Category.objects.all()

print(categories)

serializer = CategoriesSerializer(categories, many=True)  # ПО УМОЛЧАНИЮ сериализаторы ожидают ОДИН объект на вход

print(serializer.data)