from django import forms
from django.utils.translation import ugettext_lazy as _
from xtags import settings
from xtags.models import Tag
from xtags.utils import parse_tags


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag

    def clean_name(self):
        value = self.cleaned_data['name']
        tag_names = parse_tags(value)
        if len(tag_names) > 1:
            raise forms.ValidationError(_('Multiple tags were given.'))
        elif len(tag_names[0]) > settings.MAX_TAG_LENGTH:
            raise forms.ValidationError(
                _('A tag may be no more than %s characters long.') %
                    settings.MAX_TAG_LENGTH)
        return tag_names[0]


class TagField(forms.CharField):
    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            tags = parse_tags(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))

        for tag_name in tags:
            if len(tag_name) > settings.MAX_TAG_LENGTH:
                raise forms.ValidationError(
                    _('Each tag may be no more than %(length)s characters long.') % {'length': settings.MAX_TAG_LENGTH})
        return tags
