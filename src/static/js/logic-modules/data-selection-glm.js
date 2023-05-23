var current_variables_selected = -1;
var line_graph = ['date', 'int'];
var bar_graph = ['string'];
var pie_chart = ['string'];
var scatter_plot = ['date', 'int'];

export async function getResourceVariables(graph_type, resource_type, selected_variable) {
    const response = await fetch("../../static/dicts/resource_variables.json");
    const data = await response.json();
    for (var resource in data) {
        if (resource.toLowerCase() == resource_type.toLowerCase()) {
            current_variables_selected++;
            var variables = Object.entries(data[resource][0]);
            var filtered_variables = filterVariables(variables, graph_type, selected_variable);
            var interface_text = await writeInterfaceText(graph_type);
            return [current_variables_selected, interface_text, filtered_variables];

        }
    }
}

export async function getResourceFilterVariables(filter_resouce_type) {
    const response = await fetch("../../static/dicts/resource_variables.json");
    const data = await response.json();
    return data["FILTER_PARAMS"][filter_resouce_type];
}

function filterVariables(variables, graph_type, selected_variable) {
    var possible_variables = [];
    variables.forEach(variable => {
        var variable_name = variable[0];
        var variable_type = variable[1];
        var allowed_variables;
        if (graph_type == 'Line graph') {
            allowed_variables = line_graph;
        } else if (graph_type == 'Bar graph') {
            allowed_variables = bar_graph;
        } else if (graph_type == 'Pie chart') {
            allowed_variables = pie_chart;
        } else if (graph_type == 'Scatter plot') {
            allowed_variables = scatter_plot;
        }

        if (allowed_variables.includes(variable_type)) {
            if (selected_variable !== undefined && selected_variable != variable_name) {
                possible_variables.push(variable_name);
            } else if (selected_variable == undefined) {
                possible_variables.push(variable_name);
            }
        }
    });

    return possible_variables;
}

async function writeInterfaceText(graph_type) {
    if (graph_type == 'Line graph') {
        if (current_variables_selected == 0) {
            return "Select the X variable for your line graph";
        } else if (current_variables_selected >= 1) {
            return "Select the Y variable for your line graph";
        }
    } else if (graph_type == 'Bar graph') {
        if (current_variables_selected == 0) {
            return "Select the X variable for your bar graph";
        } else if (current_variables_selected >= 1) {
            return "Select the Y variable for your bar graph";
        }
    } else if (graph_type == 'Pie chart') {
        if (current_variables_selected == 0) {
            return "Select the variable you want to create a pie chart with";
        } else {
            return 1;
        }
    } else if (graph_type == 'Scatter plot') {
        if (current_variables_selected == 0) {
            return "Select the X variable for your scatter plot";
        } else if (current_variables_selected >= 1) {
            return "Select the Y variable for your scatter plot";
        }
    }
}

export function resetCurrentVariablesSelected() {
    current_variables_selected = -1;
}