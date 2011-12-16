from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic.list import ListView
from xtags.models import Tag

def autocomplete(request):
    if not request.GET.has_key("term"):
        return HttpResponse(simplejson.dumps([]), mimetype='application/json')
    else:
        q = request.GET["term"]
    limit = request.GET.get("limit", 10)
    tags = Tag.objects.filter(name__icontains = q).distinct()[:limit]
    l = sorted(list(tags), lambda x, y: cmp(y.items.all().count(), x.items.all().count()))
    tag_list = [  {'id': tag.pk, 'name': tag.name, 'count': tag.items.all().count() } for tag in l if tag]
    return HttpResponse(simplejson.dumps(tag_list), mimetype='application/json')


class TaggsFilterMixin(ListView):
    def get_queryset(self):
        tags = self.kwargs['tags'].split(',')
        queryset = super(TaggsFilterMixin, self).get_queryset()
        for tag in tags:
            queryset = queryset.filter(tags__name=tag)
        return queryset.distinct()
