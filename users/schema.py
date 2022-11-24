import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('name', 'email', 'phone')


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, name, email, phone):
        user1 = User(
            name=name,
            email=email,
            phone=phone
        )

        user1.save()
        return CreateUser(user=user1)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
