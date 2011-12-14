#from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from xtags.models import Tag, TaggedItem
from xtags.forms import TagAdminForm
from xtags.utils import merge


def tagged_items_count(obj):
    tagged_items_count = TaggedItem.objects.filter(tag=obj).count()
    return tagged_items_count
tagged_items_count.short_description = _('Tagged Items Count')


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem
    extra = 0


class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ('name', tagged_items_count)
    fieldsets = [
            (None, {'fields': ['name', 'promote',]}),
    ]
    search_fields = ('name',)
    actions = ['merge_tags']
    inlines = [
        TaggedItemInline
    ]

    def merge_tags(self, request, queryset):
        if len(queryset) > 1:
            first = queryset[0]
            tags = queryset[1:]
            for t in tags:
                merge(first, t)
    merge_tags.short_description = _("Merge selected tags")

    """
    class Media:
        if hasattr(settings, 'STATIC_URL'):
            media_url = settings.STATIC_URL
        else:
            media_url = settings.MEDIA_URL

        css = {"all": (media_url + "xtags/css/merger.css",
                       media_url + "admin/css/jquery-ui/jquery-ui.css",)}
        js = (media_url + "admin/js/jquery-ui-min.js",
              media_url + "xtags/js/merger.js")
    """


admin.site.register(Tag, TagAdmin)
