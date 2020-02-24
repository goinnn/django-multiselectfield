if (typeof jQuery === 'undefined') {
    var jQuery = django.jQuery;
}

(function ($) {
    $(function () {
        $('.sortable-item-list').each(function () {
            $(this).sortable({
                axis: 'y',
              cursor: 'move',
              items: "> .sortable-item"

            });
        });
    });
})(jQuery);