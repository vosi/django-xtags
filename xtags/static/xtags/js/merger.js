(function($){
    $(document).ready(function() {
        function recalculateRows() {
            $('#result_list tr').each(function(idx){
                if(idx/2 == Math.ceil(idx/2)) {
                    $(this).removeClass('row1').addClass('row2')
                } else {
                    $(this).removeClass('row2').addClass('row1')
                }
            })
        }
        $('#result_list tr').draggable({
            helper: function(event){
                var original = $(event.target);
                return $('<div class="drag-cart-item"><table></table></div>')
                    .find('table').append(original.closest('tr').clone()).end().appendTo('#changelist');
            },
            start: function(event, ui) {
                $(this).hide()
            },
            stop: function(event, ui) {
                $(this).show()
            }
        }).droppable({
            drop: function(event, ui) {
                var dragged = $(ui.draggable);
                var dropped = $(this);

                $('<div id="dialog-confirm">' +
                      '<p><span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 20px 0;"></span>' +
                      interpolate(gettext('Are you shure you want to marge %(tag1)s with %(tag2)s?'), {
                          tag1: '<strong>' + dragged.find('th a').text() + '</strong>',
                          tag2: '<strong>' + dropped.find('th a').text() + '</strong>'
                      }, true) +
                      '</p>' +
                  '</div>')
                .dialog({
                    resizable: false,
                    modal: true,
                    title: gettext('Comfirm merging!'),
                    buttons: [
                        {
                            text: gettext('Merge'),
                            click: function(){
                                $.ajax({
                                    url: "merge/",
                                    success: function() {
                                        dragged.remove();
                                        recalculateRows();
                                    }
                                });
                                $(this).dialog("close");
                            }
                        },{
                            text: gettext('Cancel'),
                            click:function(){
                                $(this).dialog("close");
                            }
                        }
                    ]
                })
            }
        });
    })
})(jQuery);
