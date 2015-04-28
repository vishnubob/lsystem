function modal_rules()
{
    var lsystem_modal = $("#lsystem-modal");
    $.ajax({
        type: "GET",
        url: "/rules",
        dataType: "json",
        success: function(data)
        {
            var rules = data["rules"];
            var form = $("#lsystem_rule_form");
            var rulediv = $("#lsystem_rule_form_entry");
            for (var rule in rules)
            {
                for (var subrule in rules[rule])
                {
                    var dom_rule = rulediv.clone();
                    var label = "rule_" + rule;
                    dom_rule.find("#rule_label").html(label);
                    dom_rule.find("#rule_label").attr({
                       "id": label,
                       "for": label,
                    })
                    dom_rule.find("#rule_input").attr({
                       "id": label,
                       "value": rules[rule][subrule]["rule"],
                    })
                    dom_rule.find("#weight_label").html("weight " + label);
                    dom_rule.find("#weight_label").attr({
                       "id": label + "_weight",
                       "for": label + "_weight",
                    })
                    dom_rule.find("#weight_input").attr({
                       "id": label + "_weight",
                       "value": rules[rule][subrule]["weight"],
                    })
                    form.append(dom_rule);
                }
            }
            lsystem_modal.modal("show");
        }
    });
}

function pull_draw_data()
{
    var xmlhttp = new XMLHttpRequest();
    var url = "http://localhost:5000/draw.svg";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
        {
            draw(xmlhttp.response);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function draw(svg) {
    // Make an instance of two and place it on the page.
    var elem = document.getElementById('draw-shapes').children[0];
    elem.innerHTML = svg;
}

var _timer_id = undefined;

function enable_refresh()
{
    _timer_id = setInterval(pull_draw_data, 100);
}

function disable_refresh()
{
    if (_timer_id != undefined)
    {
        clearInterval(_timer_id);
    }
}



