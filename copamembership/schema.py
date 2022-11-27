import graphene as graphene

import users.schema
import groups.schema


class Query(
    users.schema.Query,
    groups.schema.Query,
    graphene.ObjectType
    
):
    pass


class Mutation(
    users.schema.Mutation,
    groups.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
