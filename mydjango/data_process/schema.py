import graphene
from graphene_django.types import DjangoObjectType

from data_process.models import Book


class BookType(DjangoObjectType):

    class Meta:
        model = Book


class Query(graphene.ObjectType):
    books = graphene.List(BookType, title=graphene.String(), id=graphene.Int())

    def resolve_books(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        if id is not None:
            return Book.objects.filter(id=id)
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


class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title=None, content=None):
        book = Book.objects.get(id=id)

        if title:
            book.title = title
        if content:
            book.content = content

        book.save()
        return UpdateBookMutation(book=book)

class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return DeleteBookMutation(success=True)
        except Book.DoesNotExist:
            return DeleteBookMutation(success=False)
        
# 將 Mutation 加入到主 Query 類別中
class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()