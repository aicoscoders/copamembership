import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Group



class groupType(DjangoObjectType):
    class Meta:
        model=Group
        fields=('id','name','description')

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
    

    # updating the group
class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name=graphene.String(required=True)
        descr=graphene.String() 

    groupe=graphene.Field(groupType)  
    @classmethod
    def mutate(cls,root,info,name,id,descr=None):
        grp=Group.objects.get(id=id)
        grp.name=name
        grp.description=descr
        grp.save()
        return UpdateGroup(groupe=grp) 
    

class Mutation(graphene.ObjectType):
    create_group=createGroup.Field() 
    update_group=UpdateGroup.Field()  

# schema = graphene.Schema(query=Query,mutation=Mutation) 

        