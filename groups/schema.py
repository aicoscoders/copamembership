import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Group
from users.models import User
from graphql import GraphQLError




class groupType(DjangoObjectType):
    class Meta:
        model=Group
        fields=('id','name','description','users')

class Query(graphene.ObjectType):
    groupe= DjangoListField(groupType)
    group_users = graphene.Field(groupType, id=graphene.ID())

    
    def resolve_group(root,info):
        return Group.objects.all()

    def resolve_group_users(root, info, id):
        return Group.objects.get(id=id)
          

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
    error = graphene.String()

    @classmethod
    def mutate(cls,root,info,gid,uid):

        user = User.objects.filter(id=uid).first()


        if not user:
            return Add_user(error="User doesn't exist!")
        

        groupID=Group.objects.filter(id=gid).first()

        if not groupID:
            return Add_user(error="Group doesn't exist!")

        groupID.users.add(user)
        groupID.save()
        return Add_user(groupe=groupID)     

class Deletegroup_user(graphene.Mutation):
        class Arguments:
            gid = graphene.Int()
            uid=graphene.Int()
            
            
        groupe=graphene.Field(groupType)
        error=graphene.String()

        @classmethod
        def mutate(cls, root, info, uid, gid):
            user=User.objects.filter(id=uid).first()

            if not user:
                return Deletegroup_user(error="User doesn't exist!")

            group=Group.objects.get(id=gid)
            group.users.remove(user)
            
            
            return Deletegroup_user(groupe=group)


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
    add_GroupUser=Add_user.Field()
    Deletegroupuser= Deletegroup_user.Field()

 

        