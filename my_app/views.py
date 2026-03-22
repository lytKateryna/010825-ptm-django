from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import QuerySet

from my_app.models import Book
from my_app.serializers import BooksSerializer, BookCreateSerializer, BookUpdateSerializer


# получить список всех книг
@api_view(['GET'])
def get_all_books(request: Request) -> Response:
    # 1. Получить объекты из БД
    queryset: QuerySet[Book] = Book.objects.all()

    # 2. Преобюразовать в простые объекты
    serializer = BooksSerializer(queryset, many=True)  # QuerySet -> [dict[]]

    # 3. Вернуть результат
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_book_by_id(request: Request, pk: int) -> Response:
    # 1. Получить объекты из БД
    try:
        obj: Book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            data={"error": f"Book with ID {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2. Преобюразовать в простые объекты
    serializer = BooksSerializer(obj)  # QuerySet -> [dict[]]

    # 3. Вернуть результат
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def create_new_book(request: Request) -> Response:
    try:
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as err:
        return Response(
            data={"error": f"Validation error: {err}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


@api_view(['PUT', 'PATCH'])
def update_book(request: Request, pk: int) -> Response:
    try:
        obj = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            data={"error": f"Book with ID {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    partial = False if request.method == 'PUT' else True

    serializer = BookUpdateSerializer(instance=obj, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['PUT', 'PATCH'])
def delete_book(request: Request, pk: int) -> Response:
    try:
        obj = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            data={"error": f"Book with ID {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    obj.delete()

    return Response(
        data={"message": f"Book with ID {pk} deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )
