import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone')


class Query(graphene.ObjectType):
    users = graphene.List(UserType) 
    user=graphene.Field(UserType, id=graphene.ID())

    def resolve_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, id):
        return User.objects.get(id=id)


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

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name=graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        
        
    
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, name, email, phone, id):
        user_id=User.objects.get(id=id)
        user_id.name = name
        user_id.email = email
        user_id.phone = phone
        user_id.save()
        return UpdateUser(user=user_id)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
