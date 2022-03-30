function submit_from_fieldset(fieldset_id) {
    for (var i = 0; i <= document.getElementById(fieldset_id).children.length; i++) {
        try {
            if (document.getElementById(fieldset_id).children.item(i).checked) {
                document.cookie = fieldset_id + "=" + document.getElementById(fieldset_id).children.item(i).id + ";";
            }
        } catch {
            continue;
        }
    }
}

function submit_from_select(select_id) {
    document.cookie = select_id + "=" + document.getElementById("theme").value;
}

function submit() {
    submit_from_fieldset("lang");
    submit_from_select("theme");
    location.reload();
}

function uncheckOthers(id, cls) {
    if (!document.getElementById(id).checked) {
        document.getElementById(id).checked = true;
    }

    var elm = document.getElementsByClassName(cls);

    // loop through all input elm in form

    for (var i = 0; i < elm.length; i++) {
        if (elm.item(i).type == "checkbox" && elm.item(i).id != id) {
            elm.item(i).checked = false;
        }
    }
}
