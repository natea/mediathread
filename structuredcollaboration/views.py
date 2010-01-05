from structuredcollaboration.models import Collaboration
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse,resolve
from django.contrib.contenttypes.models import ContentType

# tree management (add/remove leaf)
# re-ordering
# DO NOT PROVIDE 'MOVE' (intended to be unoptimized)

def view_collaboration(request,context_slug,obj_type,obj_id):
    context = get_object_or_404(Collaboration,slug=context_slug)
    request.collaboration_context = context
    collab = get_object_or_404(Collaboration,
                               _parent=context,#will be context=context
                               content_type=ContentType.objects.get(model=obj_type),
                               object_pk=obj_id)
    if not collab.permission_to('read',request):
        return HttpResponseForbidden("forbidden")
    
    #todo:set context on request
    #Method 1. obj.default_view(request,obj)
    if hasattr(collab.content_object,'default_view'):
        return collab.content_object.default_view(request,collab.content_object)
    possible_link = reverse('%s-view' % obj_type,
                            args=[obj_id]
                            )
    #Method 2. reverse('{obj-type}-view',obj_id)
    if possible_link:
        view, args, kwargs = resolve(possible_link)
        kwargs['request'] = request
        return view(*args,**kwargs)

    return HttpResponseServerError('No method to view object %s/%s/%d' %
                                   (context_slug,obj_type,obj_id))
            
def collaboration_rss(request,context_slug):
    "RSS feed for collaboration tree"
    pass
