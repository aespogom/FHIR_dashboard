import { getResourceVariables, getResourceFilterVariables, resetCurrentVariablesSelected } from '/../static/js/logic-modules/data-selection-glm.js';

var graph_location;
var graph_type;
var resource_type;
var filter_resouce_type;

$(document).ready(function () {
    localStorage.clear();
    $("#preset-2").hide();
    $("#preset-3").hide();

    $("button[id^='preset-']").click(function () {
        var id = $(this).attr("id");
        var number = id.split("-")[1];

        $("div[id^='preset-']:visible").hide();

        $("#preset-" + number).show();
    });
});

$("#add-graph").click(function () {
 
    $('[id^="graph-location"]').bind("click", function () {
        $('[id^="graph-location"]').off("click");
        graph_location = $(this);
        if (graph_location.find(".plot-container").length > 0) {  
            alert("This container already contains a graph! Select another container or delete the current graph first.");
            return
        }
        $("#AI-help").show();
        $(graph_location).addClass("bg-secondary").removeClass("bg-light");
        $("#add-graph").next().nextAll().slice(-3).empty();
        showSelectGraph();
    });
});

function showSelectGraph() {
    $("#select-graph-div").html(`
        <br>
        <p> Select the type of graph </p>
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
        <p> Select a FHIR resource</p>
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
    $("#select-additional-filters").empty();
    showSelectDates();
    showAdditionalFilteringResource();
    $("#filter-button").show();
});

function showSelectDates() {
    $("#select-dates-div").html(`
        <br>
        <p> Optionally filter by date </p>
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date" name="start-date">
        <br>
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date" name="end-date">
        <br> <br> <p> Or you can filter your data by another resource <br>
    `);
}

var filter_variable_selection_added = false;

function showAdditionalFilteringResource() {
    $("#select-additional-filters").append(`Select a resource
    <select class="form-select select-additional-filter-resource" name="select-additional-filter-resource" value="select-additional-filter-resource">
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

$(document.body).off('change', '.select-additional-filter-resource:last').on('change', ".select-additional-filter-resource:last", function () {
    if (filter_variable_selection_added) {
        return
    }
    var filter_resource_type = $(".select-additional-filter-resource:last").val();
    showAdditionalFilteringVariable(filter_resource_type);
    filter_variable_selection_added = true;

});

async function getPossibleFilterVariables(filter_resource_type) {
    var possible_filter_variables = await getResourceFilterVariables(filter_resource_type);
    return possible_filter_variables;
}

function showAdditionalFilteringVariable(filter_resource_type) {
    var possible_filter_variables = getPossibleFilterVariables(filter_resource_type);
    var select_string = `
    <br>
    <p> Select a variable </p>
    <select class="form-select select-additional-filter-variable" name="select-additional-filter-variable" value="select-additional-filter-variable">
      <option style="display: none">Variable</option>`;
    possible_filter_variables.then((value) => {
        value.forEach(variable => {
            select_string += `<option value="${variable}">${variable}</option>`;
        });
        select_string += "</select>";
        select_string += '<br> The variable should be';
        select_string += '<br> <input type="text" class="filter-value" name="filter-value" style="max-width: 100%;">';
        select_string += '<br> <br> <button id="add-another-filter" class="btn btn-outline-dark text-white" style="background-color: #6096B4"> Add another filter </button>';

        var additionalFilters = document.createElement("div");
        additionalFilters.innerHTML = select_string;

        $("#select-additional-filters").append(additionalFilters);
    });
}

$(document.body).off('click', '#add-another-filter').on('click', "#add-another-filter", function () {
    filter_variable_selection_added = false;
    $("#add-another-filter").remove();
    showAdditionalFilteringResource();
});



$("#create-graph").off("click").on("click", function () {
    var graph_type = $("#select-graph-type").val();
    var resource = $("#select-resource").val();
    var data_element_x = $("#select-variable-0").val();
    var data_element_y = $("#select-variable-1").val() || '';
    var start_date = $('#start-date').val() ? new Date($('#start-date').val()) : null;
    var end_date = $('#end-date').val() ? new Date($('#end-date').val()) : null;

    var filter_resources = $(".select-additional-filter-resource").map((_, el) => el.value).get();
    var filter_variables = $(".select-additional-filter-variable").map((_, el) => el.value).get();
    var filter_values = $(".filter-value").map((_, el) => el.value).get();
    
    let filter_dict = new Map();
    if (filter_resources.length !== 0 && filter_variables.length !== 0 && filter_values.length !== 0) {
        filter_resources.forEach(function (key_name, i) {
            
            var dict_aux = new Map();
            filter_dict.set(key_name, dict_aux.set(filter_variables[i], filter_values[i]))
        });
    }
    filter_dict = mapToJSON(filter_dict);

    var data = JSON.stringify({ graph_type: graph_type, resource: resource, data_element_x: data_element_x, data_element_y: data_element_y, start_date: start_date, end_date: end_date, filters: filter_dict, graph_location: graph_location.attr("id") });
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

async function cb(data, graph_location) {
    $("#Go-button-text").hide();
    $("#Go-button-spinner").show();

    return new Promise(function (resolve, reject) {
        $.ajax({
            type: "POST",
            url: "/callback",
            data: data,
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                $("#Go-button-text").show();
                $('#select-graph-div').empty();
                $("#select-resource-div").empty();
                $("#select-variabele-div").empty();
                $("#AI-help").hide();
                $("#filter-button").hide();
                $("#" + graph_location).removeClass("bg-secondary").addClass("bg-light");
                Plotly.newPlot(graph_location, data, { staticPlot: true });
                if ($('#' + graph_location).find('#close-button').length === 0) {
                    var close_button = `
                <input id="close-button" type="button"
                class="btn-close bg-light" aria-label="Close" 
                onclick="$('#`+ graph_location + `').empty()" 
                style="margin-left: auto;display: block;"/>`
                    $('#' + graph_location).prepend(close_button);
                }
                $("#Go-button-spinner").hide();
                resolve();
                $("#liveToast").show();
                setTimeout(() => { $("#liveToast").hide(); }, 3000);
            },
            error: function (request, status, error) {
                alert(request.responseText);
                handleGraphTypeChange();
                $("#Go-button-spinner").hide();
                $("#Go-button-text").show();
                resolve();
            }
        });
    });
}

$("#ai-submit").click(function () {
    aigpt($("#ai-prompt").val());

})

$("#ai-prompt").keyup(function (event) {
    if (event.keyCode === 13) {
        aigpt($("#ai-prompt").val());
    }
});


function aigpt(prompt) {
    $("#ai-button-text").hide()
    $("#ai-button-spinner").show() 
    let responseText = "";
    let input_prompt = `\
        Upon receiving a free text string, the model will:
        1. Identify a type of graph mentioned in the provided list: "Line graph, Bar graph, Pie chart, Scatter plot." The model will extract the corresponding type of graph as a string.
        2. Identify a type of FHIR resource mentioned in the provided list: """AdverseEvent, AllergyIntolerance, CarePlan, ClaimResponse, Condition, DetectedIssue, InsurancePlan, Medication, Observation, Procedure, RiskAssessment, Encounter, Patient""". The model will extract the corresponding FHIR resource as a string.
        3. Extract one or two attributes related to the FHIR resource mentioned in step 2. The model will verify that the mentioned attribute(s) are included in the official FHIR R4 resource.
        4. Identify a set of filters. Each filter consists of one FHIR resource, one attribute, and one value to filter by. The filter FHIR resource should be included in the provided list: """AdverseEvent, AllergyIntolerance, CarePlan, ClaimResponse, Condition, DetectedIssue, InsurancePlan, Medication, Observation, Procedure, RiskAssessment, Encounter, Patient""". The filter FHIR resource may be different from the identified resource in step 1. The filter attribute is included in the official FHIR R4. The model will extract the corresponding set of filters as a key-value dictionary. The dictionary key will be a string corresponding to the filter resource. For each filter resource, a new key should be set. The value of the dictionary will be an embedded dictionary. The embedded dictionary has a key corresponding to the filter attribute and a value corresponding to the filter value. Exclude from the response all of the following characters: <, >, ==, != .
        The resulting keywords will be returned as a semicolon-separated string.
        If it is not possible to extract any keyword, an empty string will be returned.
        If no type of graph is mentioned and two attributes are identified, return Line graph.
        If no type of graph is mentioned and one attribute is identified, return Pie chart.
        If no FHIR resource is identified, return Observation.
        If no attributes are identified, return date and amountvalue.
        If no filters are identified, return {}.
        Free text string 1: """I want to plot patient age versus gender as bars."""
        Keywords 1: Bar graph; Patient; age; gender; {}
        ##
        Free text string 2: """Display a plot where the allergy codes are scattered against the severity from January 2023.
        Keywords 2: Scatter plot; AllergyIntolerance; code; severity; {"AllergyIntolerance": {"date": "2023-01-01"}}
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
            $("#ai-button-text").show();
            $("#ai-button-spinner").hide();
            if (response.choices && response.choices.length) {
                responseText = response.choices[0].text?.replaceAll('\n', "");
                $("#ai-result").val(responseText);
            }
        },
        error: function (request, status, error) {
            alert(request.responseText);
            $("#ai-prompt").empty();
            $("#ai-button-spinner").hide();
            $("#ai-button-text").show();
        }  
    })
}

$("#Usebutton").click(function() {
    const ai_result = $("#ai-result").val().split(";")
    let graph_name = ai_result[0].substring(1)
    let resource_name = ai_result[1]
    resource_name = resource_name.replace(" ", "")
    let x_name = ai_result[2]
    x_name = x_name.replace(" ", "")
    let y_name = ''
    if (ai_result[3] !== undefined) {
        y_name = ai_result[3].replace(" ","")
    }  
    let filter_dict = new Map();
    if (ai_result[4] !== undefined && ai_result[4].length > 0) {
        let identified_filters = JSON.parse(ai_result[4].substring(1));
        Object.keys(identified_filters).forEach(function (key_name, i) {
            filter_dict.set(key_name, identified_filters[key_name])
        });
        filter_dict=mapToJSON(filter_dict);
    }     

    var data = JSON.stringify({graph_type: graph_name,
                                resource: resource_name,
                                data_element_x: x_name,
                                data_element_y: y_name,
                                filters: filter_dict,
                                graph_location: graph_location.attr("id")});
    updateGraphStorage(data);
    cb(data, graph_location.attr("id"));
    $("#ai-prompt").val("");
    $("#ai-result").val("");
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
    var scenario_1 = '{"graph_type":"Line graph",\
    "resource":"Observation",\
    "data_element_x":"effectiveDateTime",\
    "data_element_y":"amountvalue",\
    "start_date":null,\
    "end_date":null,\
    "filters":{"value-quantity":"28,29,30,31,32,33,34,35,36,37"},\
    "graph_location": "graph-location-1"}'

    var scenario_2 = '{"graph_type":"Bar graph",\
    "resource":"Procedure",\
    "data_element_x":"performedDateTime",\
    "data_element_y":"amountvalue",\
    "start_date":null,\
    "end_date":null,\
    "filters":{"code":"CT"},\
    "graph_location": "graph-location-2"}'

    var scenario_3 = '{"graph_type":"Pie chart",\
    "resource":"Procedure",\
    "data_element_x":"code",\
    "data_element_y":"",\
    "start_date":"2020-01-01T",\
    "end_date":"2024-01-01T",\
    "filters":{},\
    "graph_location": "graph-location-3"}'

    var scenario_4 = '{"graph_type":"Line graph",\
    "resource":"Patient",\
    "data_element_x":"birthDate",\
    "data_element_y":"amountvalue",\
    "start_date":"",\
    "end_date":"",\
    "filters":{},\
    "graph_location": "graph-location-4"}'

    var scenario_5 = '{"graph_type":"Pie chart",\
    "resource":"Medication",\
    "data_element_x":"code",\
    "data_element_y":"",\
    "start_date":"",\
    "end_date":"",\
    "filters":{},\
    "graph_location": "graph-location-5"}'

    var dataArray = [scenario_1, scenario_2, scenario_3, scenario_4, scenario_5];
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

async function displayImportedGraphs() {
    var graphs = localStorage.getItem('graphs');

    if (graphs) {
        var graphs_array = JSON.parse(graphs);

        for (const graph of graphs_array) {
            var graph_location_for_import = JSON.parse(graph)["graph_location"];
            console.log(graph_location_for_import);
            await cb(graph, graph_location_for_import);
        }
    } else {
        console.log('No graphs found in localStorage.');
    }
}

function mapToJSON(map) {
    const jsonObj = {};

    map.forEach((value, key) => {
        if (typeof value === 'object' && value instanceof Map) {
        jsonObj[key] = mapToJSON(value); // Recursively convert nested map
        } else {
        jsonObj[key] = value; // Convert regular value
        }
    });

    return jsonObj;
}