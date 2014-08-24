var models = models || {};
var csrf = csrf || '';
var current;


setInput = function (el, ftype, url) {
    current = el;

    var field_type = 'text';
    if (ftype == 'int') {
        field_type = 'number';
    } else if (ftype == 'date') {
        field_type = 'text';
    }
    var name = $(el).attr('data-name');
    var dataid = $(el).attr('data-id');

    var txt = '<input data-name="' + name + '" data-id="' + dataid + '" ' +
        'type="' + field_type + '" ' +
        'onblur="save_value(this, \'' + url + '\')" style="width:98%">';
    var input = $(txt);

    input.val($(el).html().trim());
    $(el).hide();
    $(el).after(input);

    if (ftype == 'date') {
        input.removeAttr('onblur');
        input.datepicker(
            {
                dateFormat: "dd-mm-yy",
                onClose: function () {
                    save_value(input, url)
                }
            }
        );
    }

    input.focus();
};

save_value = function (el, url) {
    $(el).attr('disabled', 'disabled');

    function stop_loading() {
        $(el).removeAttr('disabled');
        $(el).focus();
    }

    var val = $(el).val();
    var itemid = $(el).attr('data-id');
    var name = $(el).attr('data-name');

    $.post(url,
        {id: itemid, field: name, value: val, csrfmiddlewaretoken: csrf},
        function (res) {
            if (res.status == 'OK') {
                $(current).html(val);
                $(el).remove();
                $(current).show();
            } else {
                alert(res.message);
                stop_loading();
            }
        }
    ).error(
        function () {
            stop_loading();
        }
    );
};

var save_form = function () {

};

var update_fields = function () {
    $('[data-type="date"]').datepicker({dateFormat: "dd-mm-yy"});
};


var load_page = function (url) {
    $.get(url, function (res) {
        build_form(res);
        build_items(res);
        update_fields();
    });
};


var build_form = function (context) {
    context.models = models;
    context.csrf = csrf;
    //noinspection JSPotentiallyInvalidConstructorUsage
    var tpl = new jSmart($("#form_template").html());
    var html = tpl.fetch(context);
    $('#form_content').html(html);
};

var build_items = function (context) {
    context.models = models;
    //noinspection JSPotentiallyInvalidConstructorUsage
    var tpl = new jSmart($("#entries_template").html());
    var html = tpl.fetch(context);
    $('#entries_content').html(html);
};