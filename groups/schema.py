import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Group
from users.models import User



class groupType(DjangoObjectType):
    class Meta:
        model=Group
        fields=('id','name','description','users')

class Query(graphene.ObjectType):
    groupe= DjangoListField(groupType)
    
    def resolve_group(root,info):
        return Group.objects.all()
          

class createGroup(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        description=graphene.String(required=True)
        users=graphene.List(graphene.Int)
     
    groupe=graphene.Field(groupType) 

    @classmethod
    def mutate(cls,root,info,name,description):
        
        group=Group(
            name=name,
            description=description,
   
        )  
        group.save()
        return createGroup(groupe=group) 
# Add user to the group    
class Add_user(graphene.Mutation):
    class Arguments:
        gid= graphene.Int()
        uid=graphene.Int()
    
    groupe=graphene.Field(groupType) 

    @classmethod
    def mutate(cls,root,info,gid,uid):

        userId= User.objects.get(id=uid)

        groupID=Group.objects.get(id=gid)

        groupID.users.add(userId)
        groupID.save()
        return Add_user(groupe=groupID)  


class ErrorType(graphene.ObjectType):
    field=graphene.String()
    message=graphene.String()


    # updating the group
class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name=graphene.String()
        descr=graphene.String() 

    groupe=graphene.Field(groupType)
    error=graphene.Field(ErrorType)
    @classmethod
    def mutate(cls,root,info,name=None,id=None,descr=None):
        grp=Group.objects.filter(id=id).first()
        if not grp:
            err = {
                "field":"id",
                "message":"provide the valid group id"
            }
            return UpdateGroup(error=err)
        grp.name=name
        grp.description=descr
        grp.save()
        return UpdateGroup(groupe=grp) 
    

class Mutation(graphene.ObjectType):
    create_group=createGroup.Field() 
    update_group=UpdateGroup.Field()  
    add_GroupUser=Add_user.Field()

 

        