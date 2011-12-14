from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from xtags.utils import edit_string_for_tags


class TagAutoCompleteInput(forms.TextInput):

    class Media:
        if hasattr(settings, 'STATIC_URL'):
            media_url = settings.STATIC_URL
        else:
            media_url = settings.MEDIA_URL

        css = {"all": (media_url + "admin/css/jquery-ui/jquery-ui.css",)}
        js = (media_url + "admin/js/jquery-ui-min.js",)

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
        output = super(TagAutoCompleteInput, self).render(name, value, attrs)
        return output + mark_safe(u"""
            <script type="text/javascript">
            (function($){
                $(document).ready(function() {
                    function split( val ) {
		            	return val.split( /,\s*/ );
		            }
		            function extractLast( term ) {
			            return split( term ).pop();
		            }
                    $("#id_%(id)s").bind("keydown", function(event) {
				        if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active) {
					        event.preventDefault();
    				    }
	    		    }).autocomplete({
                        source: function( request, response ) {
                            $.ajax({
                                url: "%(url)s",
                                dataType: "json",
                                data: {term: extractLast(request.term)},
                                success: function(data) {
                                    response($.map(data, function(item) {
                                        return {
                                            label: item.name + " (" + item.count + ")",
                                            value: item.name
                                        }
                                    }));
                                }
                            });
                        },
                        search: function() {
                            var term = extractLast( this.value );
                            if ( term.length < 1 ) {
                                return false;
                            }
                        },
                        focus: function() {
                            return false;
                        },
                        select: function( event, ui ) {
                            var terms = split( this.value );
                            terms.pop();
                            terms.push( ui.item.value );
                            terms.push( "" );
                            this.value = terms.join( ", " );
                            return false;
                        }
	    		    });
	    		});
	    	})(jQuery);
            </script>""" % {'id':name,'url': reverse("tagging_ext_autocomplete")}
        )
