import { getResourceVariables, resetCurrentVariablesSelected } from '/../static/js/logic-modules/data-selection-glm.js';

var graph_location;
var graph_type;
var resource_type;
var filter_resouce_type;
$("#add-graph").click(function () {
    $('[id^="graph-location"]').bind("click", function () {
        $("#AI-help").show()
        $('[id^="graph-location"]').off("click");
        graph_location = $(this);
        $(graph_location).addClass("bg-secondary").removeClass("bg-light");
        $("#add-graph").next().nextAll().empty();
        showSelectGraph();
    });
});

function showSelectGraph() {
    $("#select-graph-div").html(`
        <br>
        <p> Select the type of graph you want to create </p>
        <select class="form-select" id="select-graph-type" name="select-graph-type" value="select-graph-type">
            <option style="display: none">Graph type</option>
            <option value="Bar graph">Bar graph</option>
            <option value="Line graph">Line graph</option>
            <option value="Pie chart">Pie chart</option>
            <option value="Scatter plot">Scatter plot</option>
        </select>
    `);
}

function handleGraphTypeChange() {
    $("#select-resource-div").empty();
    $("#select-variabele-div").add($("#select-variabele-div").nextAll()).empty();
    resetCurrentVariablesSelected();
    graph_type = $("#select-graph-type option:selected").val();
    showSelectResource();
}

$(document.body).off('change', '#select-graph-type').on('change', "#select-graph-type", handleGraphTypeChange);

function showSelectResource() {
    $("#select-resource-div").html(`
        <br>
        <p> Now select the a resource for which you want to create a graph </p>
        <select class="form-select" id="select-resource" name="select-resource" value="select-resource">
            <option style="display: none">Resource</option>
            <option value="AdverseEvent">Adverse event</option>
            <option value="AllergyIntolerance">Allergies</option>
            <option value="CarePlan">Careplans</option>
            <option value="ClaimResponse">Claims</option>
            <option value="Condition">Conditions</option>
            <option value="DetectedIssue">Detected issues</option>
            <option value="Encounter">Encounters</option>
            <option value="InsurancePlan">Insurance plans</option>
            <option value="Medication">Medications</option>
            <option value="Observation">Observations</option>
            <option value="Patient">Patients</option>
            <option value="Procedure">Procedures</option>
            <option value="RiskAssessment">Risk assessments</option>
        </select>
    `);
}

async function handleResourceChange() {
    $(this).off('change');
    $("#select-variabele-div").empty();
    $("#select-variabele-div").nextAll().empty();
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
        if (graph_type !== "Pie chart") {
            $(this).nextAll().remove();
            $("#select-variabele-div").nextAll().empty();
        }
        var selected_variable = $("#select-variable-0 option:selected").val();
        await getPossibleVariables(selected_variable);
    });
}

$(document.body).off('change', '#select-resource').on('change', "#select-resource", handleResourceChange);

function showSelectVariable(current_number_of_variables_selected, interface_text, possible_variables) {
    var select_string = `
        <br>
        <p> ${interface_text} </p>
        <select class="form-select" id="select-variable-${current_number_of_variables_selected}" name="select-variabele-${current_number_of_variables_selected}" value="select-variabele-${current_number_of_variables_selected}">
            <option style="display: none">Variable</option>`;
    possible_variables.forEach(variable => {
        select_string += `<option value="${variable}">${variable}</option>`;
    });
    select_string += "</select>";
    $("#select-variabele-div").append(select_string);
}

$(document.body).off('change', '#select-variabele-div select:last').on('change', "#select-variabele-div select:last", function () {
    showSelectDates();
    showAdditionalFilteringResource();
});

function showSelectDates() {
    $("#select-dates-div").html(`
        <br>
        <p> Optionally you can select a start and end date for your data selection to plot a part of the data </p>
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date" name="start-date">
        <br>
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date" name="end-date">
    `);
}

function showAdditionalFilteringResource() {
    $("#select-additional-filters").html(`
        <br>
        <p> Or you can filter your data by another resource <br> For this, first select a resource </p>
        <select class="form-select" id="select-additional-filter-resource" name="select-additional-filter-resource" value="select-additional-filter-resource">
            <option style="display: none">Resource</option>
            <option value="AdverseEvent">Adverse event</option>
            <option value="AllergyIntolerance">Allergies</option>
            <option value="CarePlan">Careplans</option>
            <option value="ClaimResponse">Claims</option>
            <option value="Condition">Conditions</option>
            <option value="DetectedIssue">Detected issues</option>
            <option value="Encounter">Encounters</option>
            <option value="InsurancePlan">Insurance plans</option>
            <option value="Medication">Medications</option>
            <option value="Observation">Observations</option>
            <option value="Patient">Patients</option>
            <option value="Procedure">Procedures</option>
            <option value="RiskAssessment">Risk assessments</option>
        </select>
    `);
}

$(document.body).off('change', '#select-additional-filter-resource').on('change', "#select-additional-filter-resource", function () {
    filter_resouce_type = $("#select-additional-filter-resource").val();
    showAdditionalFilteringVariable();
});

async function getPossibleFilterVariables() {
    var possible_filter_variables = await getResourceVariables(graph_type, filter_resouce_type);
    return possible_filter_variables[2];
}

function showAdditionalFilteringVariable() {
    var possible_filter_variables = getPossibleFilterVariables();
    var select_string = `
        <br>
        <p> And select a variable </p>
        <select class="form-select" id="select-additional-filter-variable" name="select-additional-filter-variable" value="select-additional-filter-variable">
            <option style="display: none">Variable</option>`;
    possible_filter_variables.then((value) => {
        value.forEach(variable => {
            select_string += `<option value="${variable}">${variable}</option>`;
        });
        select_string += "</select>";
        $("#select-additional-filters").append(select_string);
    });
}

$("#create-graph").off("click").on("click", function () {
    var graph_type = $("#select-graph-type").val();
    var resource = $("#select-resource").val();
    var data_element_x = $("#select-variable-0").val();
    var data_element_y = $("#select-variable-1").val() || '';
    var start_date = $('#start-date').val() ? new Date($('#start-date').val()) : null;
    var end_date = $('#end-date').val() ? new Date($('#end-date').val()) : null;
    var additional_filter_resource = $("#select-additional-filter-resource").val() || null;
    var additional_filter_variable = $("#select-additional-filter-variable").val() || null;
    var data = JSON.stringify({ graph_type: graph_type, resource: resource, data_element_x: data_element_x, data_element_y: data_element_y, start_date: start_date, end_date: end_date, additional_filter_resource: additional_filter_resource, additional_filter_variable: additional_filter_variable, graph_location: graph_location.attr("id") });
    updateGraphStorage(data);
    cb(data, graph_location.attr("id"));

});

function updateGraphStorage(graph) {
    var graph_data = localStorage.getItem("graphs");
    var graph_data = graph_data ? JSON.parse(graph_data) : [];
    graph_data.push(graph);
    var updated_graph_data = JSON.stringify(graph_data);
    localStorage.setItem("graphs", updated_graph_data);
}

function cb(data, graph_location) {
    $("#Go-button-text").hide()
    $("#Go-button-spinner").show()
    $.ajax({
        type: "POST",
        url: "/callback",
        data: data,
        contentType: "application/json",
        dataType: 'json',
        success: function (data) {
            $("#Go-button-text").show();
            $("#"+graph_location).removeClass("bg-secondary").addClass("bg-light");
            Plotly.newPlot(graph_location, data, {staticPlot: true});
            if ($('#'+graph_location).find('#close-button').length === 0){
                var close_button = `
                <input id="close-button" type="button"
                class="btn-close bg-light" aria-label="Close" 
                onclick="$('#`+graph_location+`').empty()" 
                style="margin-left: auto;display: block;"/>`
                $('#'+graph_location).prepend(close_button);
            }
            $("#Go-button-spinner").hide();
        },
    })
}

$("#ai-submit").click(function () {
    aigpt($("#ai-prompt").val());
    
})

$("#ai-prompt").keyup(function(event) {
    if (event.keyCode === 13) {
        aigpt($("#ai-prompt").val());
    }
});


function aigpt(prompt) {
    $("#ai-button-text").hide()
    $("#ai-button-spinner").show() 
    let input_prompt = `\
        Upon receiving a free text string, the model will:
        1. Identify a type of graph mentioned in the provided list: "Line graph, Bar graph, Pie chart, Scatter plot." The model will extract the corresponding type of graph as a string.
        2. Identify a type of FHIR resource mentioned in the provided list: """AdverseEvent, AllergyIntolerance, CarePlan, ClaimResponse, Condition, DetectedIssue, InsurancePlan, Medication, Observation, Procedure, RiskAssessment, Encounter, Patient""". The model will extract the corresponding FHIR resource as a string.
        3. Extract one or two attributes related to the FHIR resource mentioned in step 2. The model will verify that the mentioned attribute(s) are included in the official FHIR R4 resource.
        4. Identify a set of filters. Each filter consists of one FHIR resource, one attribute, and one value to filter by. The filter FHIR resource should be included in the provided list: """AdverseEvent, AllergyIntolerance, CarePlan, ClaimResponse, Condition, DetectedIssue, InsurancePlan, Medication, Observation, Procedure, RiskAssessment, Encounter, Patient""". The filter FHIR resource may be different from the identified resource in step 1. The filter attribute is included in the official FHIR R4. The model will extract the corresponding set of filters as a key-value dictionary. The dictionary key will be a string corresponding to the filter resource. For each filter resource, a new key should be set. The value of the dictionary will be an embedded dictionary. The embedded dictionary has a key corresponding to the filter attribute and a value corresponding to the filter value. Exclude from the response all of the following characters: <, >, ==, != .
        The resulting keywords will be returned as a comma-separated string.
        If it is not possible to extract any keyword, an empty string will be returned.
        If no type of graph is mentioned and two attributes are identified, return Line graph.
        If no type of graph is mentioned and one attribute is identified, return Pie chart.
        If no FHIR resource is identified, return Observation.
        If no attributes are identified, return date and amountvalue.
        If no filters are identified, return {}.
        Free text string 1: """I want to plot patient age versus gender as bars."""
        Keywords 1: Bar graph, Patient, age, gender, {}
        ##
        Free text string 2: """Display a plot where the allergy codes are scattered against the severity from January 2023.
        Keywords 2: Scatter plot, AllergyIntolerance, code, severity, {'AllergyIntolerance': {'date': '2023-01-01'}}
        ##
        Free text string 3: """${prompt}"""
        Keywords 3:
    `
    $.ajax({
        type: "POST",
        url: "/generate",
        data: JSON.stringify({ 
            "prompt": input_prompt
        }),
        contentType: "application/json",
        dataType: 'json',
        success: function (response) {
            console.log(response);
            $("#ai-button-text").show()
            $("#ai-button-spinner").hide()
            if (response.choices && response.choices.length) {
                responseText = response.choices[0].text?.replaceAll('\n', "");
                $("#ai-result").text(responseText);
            }
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }  
    })
}

$("#Usebutton").click(function() {
    const MyArray = $("#ai-result").val().split(",")

    let varplot = MyArray[0]
    let varresource1 = MyArray[1]
    let varresource = varresource1.replace(" ","")
    let varvar1 = MyArray[2]
    let varvar = varvar1.replace(" ","")
    let var2var = ''
    if (MyArray[3] !== undefined) {
        let var2var1 = MyArray[3]
        var2var = var2var1.replace(" ","")
    }  
    let identified_filters = {}
    if (MyArray[4] !== '{}') {
        identified_filters = MyArray[3]
    }     

    var data = JSON.stringify({graph_type: varplot,
                                resource: varresource,
                                data_element_x: varvar,
                                data_element_y: var2var,
                                filters: identified_filters});
    cb(data, graph_location.attr("id"));
})

$(window).on('resize', function () {
    var graphs = $(".js-plotly-plot");

    graphs.each(function () {
        var parentWidth = $(this).parent().width();
        var parentHeight = $(this).parent().height();

        Plotly.relayout(this, { width: parentWidth, height: parentHeight });
    });
});

$("#generate-data").click(function () {
    var jsonString = '{"graph_type":"Pie chart","resource":"AllergyIntolerance","data_element_x":"text","data_element_y":"","start_date":null,"end_date":null,"additional_filter_resource":"Resource","additional_filter_variable":null}';
    var dataArray = [jsonString, jsonString, jsonString];
    localStorage.setItem("graphs", JSON.stringify(dataArray));
})

$('#export').click(function () {
    var graph_data = localStorage.getItem('graphs');
    var filename = 'dashboard.json';
    var blob = new Blob([graph_data], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

$('#import').click(function () {
    var input = document.createElement('input');
    input.type = 'file';
    input.onchange = function (e) {
        var file = e.target.files[0];
        var reader = new FileReader();

        reader.onload = function () {
            var fileContent = reader.result;
            localStorage.setItem('graphs', fileContent);
            displayImportedGraphs();
        };
        reader.readAsText(file);
    };
    input.click();
});

function displayImportedGraphs() {
    var graphs = localStorage.getItem('graphs');

    if (graphs) {
        var graphs_array = JSON.parse(graphs);
        graphs_array.forEach(function (graph) {
            var graph_location_for_import = JSON.parse(graph)["graph_location"];
            cb(graph, graph_location_for_import);
        });
    } else {
        console.log('No graphs found in localStorage.');
    }
}
