from django.contrib.contenttypes.models import ContentType
from django.db import models
from xtags.models import Tag, TaggedItem


class ModelTagManager(models.Manager):
    """
    A manager for retrieving tags for a particular model.
    """
    def get_query_set(self):
        ctype = ContentType.objects.get_for_model(self.model)
        return Tag.objects.filter(
            items__content_type__pk=ctype.pk).distinct()

    def cloud(self, *args, **kwargs):
        return Tag.objects.cloud_for_model(self.model, *args, **kwargs)

    def related(self, tags, *args, **kwargs):
        return Tag.objects.related_for_model(tags, self.model, *args, **kwargs)

    def usage(self, *args, **kwargs):
        return Tag.objects.usage_for_model(self.model, *args, **kwargs)


class ModelTaggedItemManager(models.Manager):
    """
    A manager for retrieving model instances based on their tags.
    """
    def related_to(self, obj, queryset=None, num=None):
        if queryset is None:
            return TaggedItem.objects.get_related(obj, self.model, num=num)
        else:
            return TaggedItem.objects.get_related(obj, queryset, num=num)

    def with_all(self, tags, queryset=None):
        if queryset is None:
            return TaggedItem.objects.get_by_model(self.model, tags)
        else:
            return TaggedItem.objects.get_by_model(queryset, tags)

    def with_any(self, tags, queryset=None):
        if queryset is None:
            return TaggedItem.objects.get_union_by_model(self.model, tags)
        else:
            return TaggedItem.objects.get_union_by_model(queryset, tags)
