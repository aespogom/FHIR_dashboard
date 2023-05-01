// Custom Javascript
var graph_location
var graph_type
var resource_type

$("#add-graph").click(function() {
    $('[id^="graph-location"]').bind("click", function() {
        $('[id^="graph-location"]').off("click"); 
        graph_location = $(this);
        $(graph_location).addClass("bg-secondary").removeClass("bg-light");
        showSelectGraph();
    })
})

function showSelectGraph() {
    $("#select-graph").html(`
        <br>
        <p> Select the type of graph you want to create </p>
        <select class="form-select" id="select-graph-type" name=select-graph-type" value="select-graph-type">
        <option>Graph type</option>
        <option value="Bar graph">Bar graph</option>
        <option value="Line graph">Line graph</option>
        <option value="Pie chart">Pie chart</option>
        </select>
    `);
}

$(document.body).on('change',"#select-graph-type",function () {
    graph_type = $("#select-graph-type option:selected").val();
    showSelectResource();
});

function showSelectResource() {
    $("#select-resource").html(`
        <br>
        <p> Now select the a resource for which you want to create a graph </p>
        <select class="form-select" id="select-resource" name="select-resource" value="select-resource">
        <option>Resource</option>
        <option value="Patient">Patient</option>
        <option value="Medication">Medication</option>
        <option value="Allergies">Allergies</option>
        </select>
    `);
}

$(document.body).on('change',"#select-resource",function () {
    resource_type = $("#select-resource option:selected").val();
    $(graph_location).html("Hier komt nu een " + graph_type + " van data " + resource_type);
});