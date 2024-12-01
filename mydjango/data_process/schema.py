import graphene
from graphene_django.types import DjangoObjectType

from data_process.models import Book


class BookType(DjangoObjectType):

    class Meta:
        model = Book


class Query(graphene.ObjectType):
    books = graphene.List(BookType, title=graphene.String())

    def resolve_books(self, info, **kwargs):
        title = kwargs.get('title')
        if title is not None:
            return Book.objects.filter(title__contains=title)
        return Book.objects.all()