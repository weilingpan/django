import graphene

import data_process.schema


class Query(data_process.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)