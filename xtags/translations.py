from modeltranslation.translator import translator, TranslationOptions
from xtags.models import Tag


class TagTranslation(TranslationOptions):
    fields = ('name',)


translator.register(Tag, TagTranslation)
