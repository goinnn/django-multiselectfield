(function ($) {
    $(document).ready(function () {
        $(".ui-pre-sortable").sortable({ revert: true });
    });
})(typeof django !== "undefined" && django.jQuery ? django.jQuery : jQuery);