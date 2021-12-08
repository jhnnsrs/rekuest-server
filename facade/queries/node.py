from facade.filters import NodeFilter
from typing_extensions import Annotated
from balder.types import BalderQuery
from facade import types
from facade.models import Node, Template
import graphene
from lok import bounced


class NodeDetailQuery(BalderQuery):
    class Arguments:
        q = graphene.String(description="The identifier string")
        id = graphene.ID(description="The query node")
        package = graphene.String(description="The package of this node")
        interface = graphene.String(description="The interface of this node")
        template = graphene.ID(
            description="Get node for a template (overrides the others)"
        )

    @bounced(anonymous=True)
    def resolve(root, info, template=None, **kwargs):
        if template:
            return Template.objects.get(id=template).node
        return Node.objects.get(**kwargs)

    class Meta:
        type = types.Node
        operation = "node"


class Nodes(BalderQuery):
    class Meta:
        type = types.Node
        list = True
        filter = NodeFilter
