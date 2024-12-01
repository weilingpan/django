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
    
# 定義 Mutation 類別
class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    book = graphene.Field(BookType)

    # mutate 方法
    def mutate(self, info, title, content):
        # 創建一個新的書籍實體
        book = Book.objects.create(title=title, content=content)
        return CreateBookMutation(book=book)

# 將 Mutation 加入到主 Query 類別中
class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()