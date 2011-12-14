from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r'^autocomplete/',
        'xtags.views.autocomplete', name='tagging_ext_autocomplete'),
)
