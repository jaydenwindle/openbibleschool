import graphene

import learning.schema

class Query(learning.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)