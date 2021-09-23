from facade.enums import RepositoryType
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from facade.filters import NodesFilter, ProvisionLogFilter, TemplateFilter, ProvisionFilter
from balder.fields.filtered import BalderFiltered
from django.utils.translation import templatize
from facade.structures.ports.returns.types import ReturnPort
from facade.structures.ports.kwargs.types import KwargPort
from facade.structures.ports.args.types import ArgPort
from facade import models
from lok.models import LokApp as HerreAppModel
from balder.types import BalderObject
import graphene
from balder.registry import register_type

class ReserveParamsInput(graphene.InputObjectType):
    auto_provide = graphene.Boolean(description="Do you want to autoprovide", required=False)
    auto_unprovide = graphene.Boolean(description="Do you want to auto_unprovide", required=False)
    providers = graphene.List(graphene.Int, description="Apps that you can reserve on", required=False)
    templates = graphene.List(graphene.Int, description="Apps that you can reserve on", required=False)

class ReserveParams(graphene.ObjectType):
    auto_provide = graphene.Boolean(description="Autoproviding")
    auto_unprovide = graphene.Boolean(description="Autounproviding")

class ProvideParams(graphene.ObjectType):
    auto_unprovide = graphene.Boolean(description="Do you want to auto_unprovide")



class LokApp(BalderObject):

    class Meta:
        model = HerreAppModel


class LokUser(BalderObject):

    class Meta:
        model = get_user_model()


class DataPoint(BalderObject):
    distinct = graphene.String()

    def resolve_distinct(root, info, *args, **kwargs):
        return root.app.name

    class Meta:
        model = models.DataPoint



class Structure(BalderObject):


    class Meta:
        model = models.Structure

class Scan(graphene.ObjectType):
    ok = graphene.Boolean()


class DataQuery(graphene.ObjectType):
    point = graphene.Field(DataPoint, description="The queried Datapoint")
    structures = graphene.List(Structure, description="The queried models on the Datapoint")


class Provider(BalderObject):
    
    class Meta:
        model = models.Provider

class ReservationLog(BalderObject):

    class Meta:
        model = models.ReservationLog
        

class Assignation(BalderObject):
    
    class Meta:
        model = models.Assignation


class AssignationLog(BalderObject):
    
    class Meta:
        model = models.AssignationLog

class ProvisionLog(BalderObject):
    
    class Meta:
        model = models.ProvisionLog





class Provision(BalderObject):
    params = graphene.Field(ProvideParams)
    log = BalderFiltered(ProvisionLog, filterset_class=ProvisionLogFilter, related_field="log")
    
    class Meta:
        model = models.Provision

        
class Template(BalderObject):
    provisions = BalderFiltered(Provision, filterset_class=ProvisionFilter, related_field="provisions")
    
    class Meta:
        model = models.Template

class Node(BalderObject):
    args = graphene.List(ArgPort)
    kwargs = graphene.List(KwargPort)
    returns = graphene.List(ReturnPort)
    templates = BalderFiltered(Template, filterset_class=TemplateFilter, related_field="templates")

    class Meta:
        model = models.Node

@register_type
class Repository(graphene.Interface):
    "NNanananna"
    id = graphene.ID(description="Id of the Repository")
    nodes = BalderFiltered(Node, filterset_class=NodesFilter, related_field="nodes")
    name = graphene.String(description="The Name of the Repository")

    @classmethod
    def resolve_name(cls, instance, info):
        return instance.name

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = {
            "AppRepository": lambda: AppRepository,
            "MirrorRepository": lambda: MirrorRepository
        }
        _type = instance.__class__.__name__
        return typemap.get(_type)()




@register_type
class AppRepository(BalderObject):

    class Meta:
        model = models.AppRepository
        interfaces = (Repository,)


@register_type
class MirrorRepository(BalderObject):

    class Meta:
        model = models.MirrorRepository
        interfaces = (Repository,)



class Reservation(BalderObject):
    params = graphene.Field(ReserveParams)
    
    class Meta:
        model = models.Reservation




