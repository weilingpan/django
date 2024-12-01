import graphene

import data_process.schema


class Query(data_process.schema.Query, graphene.ObjectType):
    pass

class Mutation(data_process.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)