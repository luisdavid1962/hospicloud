jQuery(document).ready(function() {
    jQuery('input.datetimepicker').datetimepicker();
    jQuery('input.datepicker').datetimepicker({
        pickTime: false
    });
    jQuery('input.future-datepicker').datetimepicker({
        pickTime: false
    });
});
