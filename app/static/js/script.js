// Custom Javascript
import { getResourceVariables, resetCurrentVariablesSelected } from '/../static/js/logic-modules/data-selection-glm.js';

var graph_location
var graph_type
var resource_type


$("#add-graph").click(function () {
    $('[id^="graph-location"]').bind("click", function () {
        $('[id^="graph-location"]').off("click");
        graph_location = $(this);
        $(graph_location).addClass("bg-secondary").removeClass("bg-light");
        $("#add-graph").nextAll().empty();
        showSelectGraph();
    })
})

function showSelectGraph() {
    $("#select-graph-div").html(`
        <br>
        <p> Select the type of graph you want to create </p>
        <select class="form-select" id="select-graph-type" name=select-graph-type" value="select-graph-type">
        <option style="display: none">Graph type</option>
        <option value="Bar graph">Bar graph</option>
        <option value="Line graph">Line graph</option>
        <option value="Pie chart">Pie chart</option>
        </select>
    `);
}

$(document.body).off('change', '#select-graph-type').on('change', "#select-graph-type", function () {
    $("#select-resource-div").empty();
    $("#select-variabele-div").empty();
    resetCurrentVariablesSelected();
    graph_type = $("#select-graph-type option:selected").val();
    showSelectResource();
});

function showSelectResource() {
    $("#select-resource-div").html(`
        <br>
        <p> Now select the a resource for which you want to create a graph </p>
        <select class="form-select" id="select-resource" name="select-resource" value="select-resource">
        <option style="display: none">Resource</option>
        <option value="Careplans">Careplans</option>
        <option value="Allergies">Allergies</option>
        </select>
    `);
}

$(document.body).off('change', '#select-resource').on('change', "#select-resource", async function () {
    $(this).off('change');
    $("#select-variabele-div").empty();
    resetCurrentVariablesSelected();
    resource_type = $("#select-resource option:selected").val();

    async function getPossibleVariables(selected_variable) {
        var [current_number_of_variables_selected, interface_text, possible_variables] = await getResourceVariables(graph_type, resource_type, selected_variable);
        if (interface_text != 1) {
            showSelectVariable(current_number_of_variables_selected, interface_text, possible_variables);
        }
        
    }

    await getPossibleVariables();

    $(document.body).off('change', '#select-variable-0').on('change', "#select-variable-0", async function () {
        $(this).off('change');
        $(this).nextAll().remove();
        var selected_variable = $("#select-variable-0 option:selected").val();
        await getPossibleVariables(selected_variable);
    })
});

function showSelectVariable(current_number_of_variables_selected, interface_text, possible_variables) {
    var select_string = `
        <br>
        <p> ` + interface_text + ` </p>
        <select class="form-select" id="select-variable-` + current_number_of_variables_selected + `" name="select-variabele-` + current_number_of_variables_selected + `" value="select-variabele-` + current_number_of_variables_selected + `">
        <option style="display: none">Variabele</option>
        `;
    possible_variables.forEach(variabele => {
        select_string += '<option value="' + variabele + '">' + variabele + '</option>'
    });
    select_string += "</select >"
    $("#select-variabele-div").append(select_string);
}