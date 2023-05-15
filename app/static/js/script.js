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
        $("#add-graph").next().nextAll().empty();
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
        <option value="Scatter plot">Scatter plot</option>
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

$("#create-graph").off("click").on("click", function() {
    var graph_type = $("#select-graph-type").val();
    var resource = $("#select-resource").val();
    var data_element_x = $("#select-variable-0").val().toUpperCase();
    if($("#select-variable-1").val()) {
        var data_element_y = $("#select-variable-1").val().toUpperCase();
    } else {
        var data_element_y = '';
    }
    var data = JSON.stringify({graph_type: graph_type, resource: resource, data_element_x: data_element_x, data_element_y: data_element_y});
    cb(data);
})


function cb(data) {
    $.ajax({
        type: "POST",
        url: "/callback",
        data: data,
        contentType: "application/json",
        dataType: 'json',
        success: function (data) {
            Plotly.newPlot(graph_location[0], data, {staticPlot: true});;
        },
    })
}

// $("#graph-locations").resizable({
//     resize: function(event, ui) {
//         var parentwidth = $("#container").innerWidth();
//         var parentheight = $("#container").innerHeight();
//         $("#child").css({'width':parentwidth, 'height':parentheight});
//     }
//  });

// function resizePlotContainers() {
//     console.log(1);
//     $('.svg-container').each(function() {
//         console.log(2);
//         var parentDiv = $(this).parent();
//         console.log(parentDiv);
//         var width = parentDiv.width();
//         var height = parentDiv.height();

//         $(this).css('width', width + 'px');
//         $(this).css('height', height + 'px');
//     });
//   }

//   $(window).resize(resizePlotContainers);
//   resizePlotContainers(); // Initial resize on page load
//   console.log(3);