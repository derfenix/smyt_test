var models = models || {};
var csrf = csrf || '';
var current;


/*
 Replace value by input
 */
//noinspection JSUnusedGlobalSymbols
function setInput(el, ftype, url) {
    if (current) {
        // Already exists input field, should be saved before create new input
        return;
    }

    current = el;

    // Select field's type
    var field_type = 'text';
    if (ftype == 'int') {
        field_type = 'number';
    }

    var name = $(el).attr('data-name');
    var dataid = $(el).attr('data-id');

    // Genereate input
    var txt = '<input data-name="' + name + '" data-id="' + dataid + '" ' +
        'type="' + field_type + '" ' +
        'onblur="save_value(this, \'' + url + '\')" style="width:98%">';
    var input = $(txt);

    // Attach input and hide text
    input.val($(el).html().trim());
    $(el).hide();
    $(el).after(input);

    // Attach datepicker to the fields with data-id="date"
    if (ftype == 'date') {
        // Remove onblur event
        input.removeAttr('onblur');
        //noinspection JSUnusedGlobalSymbols
        input.datepicker(
            {
                dateFormat: "dd-mm-yy",
                onClose: function () {
                    // Attach save_value on datepicker close event
                    save_value(input, url)
                }
            }
        );
    }

    input.focus();
}


/*
 Save input's value and remove input if save success
 */
function save_value(el, url) {
    // Disable input while trying to save value
    $(el).attr('disabled', 'disabled');

    /*
     Restore input state (enable it) and put focus
     */
    function stop_loading() {
        $(el).removeAttr('disabled');
        $(el).focus();
    }

    var val = $(el).val();
    var itemid = $(el).attr('data-id');
    var name = $(el).attr('data-name');

    // Send post request
    $.post(url,
        {id: itemid, field: name, value: val, csrfmiddlewaretoken: csrf},
        function (res) {
            if (res.status == 'OK') {
                // On success replace text by input's value
                $(current).html(val);
                $(el).remove();  // Remove input from DOM
                $(current).show(); // Show text value
                current = null;
            } else {
                // On failure - show error message and restore input state
                alert(res.message);
                stop_loading();
            }
        }
    ).error(
        function () {
            stop_loading();
        }
    );
}


/*
 Update inputs attributes and/or bindings
 */
function update_inputs() {
    $('[data-type="date"]').datepicker({dateFormat: "dd-mm-yy"});
    $('input:submit').on('click', function (e) {
        e.preventDefault();
        save_form($(e.target).parent('fieldset'));
    });
}

/*
 Save form data
 */
function save_form(el) {
    var url = $(el).parent('form').attr('action');
    var data = {csrfmiddlewaretoken: csrf, new: 1};

    $(el).find('input:text').each(
        function () {
            var e = $(this);
            data[e.attr('name')] = e.val();
        }
    );
    $.post(url, data,
        function (res) {
            build('form', res);
            build('entries', res);
            update_inputs();
        }
    );
}

/*
 Build page from templates and context
 */
function build(target, context) {
    context.models = models;
    context.csrf = csrf;
    //noinspection JSPotentiallyInvalidConstructorUsage
    var tpl = new jSmart($('#' + target + '_template').html());
    var html = tpl.fetch(context);
    $('#' + target + '_content').html(html);
}

/*
 Load page by url and proccess data
 */
function load_page(url) {
    $.get(url, function (res) {
        build('form', res);
        build('entries', res);
        update_inputs();
    });
}