// Show all sheet music
function getAllMusic() {

    var strHTMLcontent = ""; // insert search result

    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/music',
        type: 'GET',
        dataType: 'json',
        success: successFunctionAll,
        error: errorFunctionAll,
    });

    return false;
}

// Display all movies in a table
function successFunctionAll(result) {
    $('#infoSearch').html("");
    strHTMLcontent = "<table id=\"results\"><tr>" +
        "<th>Catalogue Number</th>" +
        "<th>Title</th>" +
        "<th>Composer</th>" +
        "<th>Arranger</th>" +
        "<th>Publisher</th>" +
        "<th>Featured Instrument</th>" +
        "<th>Ensemble Type</th>" +
        "<th>Parts</th>" +
        "<th>Remarks</th>" +
        "<th>Delete</th>" +
        "</tr>";

    var jObjects = result.Music
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
            let musicID = result.Music[index].musicID

            strHTMLcontent += "<tr>"+
            // Data
            "<td>" + result.Music[index].catalogueNo + "</td>" +
            "<td>" + result.Movies[index].title + "</td>" +
            "<td>" + result.Movies[index].composer + "</td>" +
            "<td>" + result.Movies[index].arranger + "</td>" +
            "<td>" + result.Movies[index].publisher + "</td>" +
            "<td>" + result.Movies[index].featuredInstrument + "</td>" +
            "<td>" + result.Movies[index].ensembleID + "</td>" +
            "<td>" + result.Movies[index].parts + "</td>" +
            "<td>" + result.Movies[index].remarks + "</td>" +

            // delete button
            "<td>" + "<a href='#' class='btn btn-default btn-danger rounded-circle px-3' onclick='return deleteMovieByID("+movID+")'>" + "X" +"</a>" + "</td>";
        }
    }
    else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#infoSearch').html(strHTMLcontent);
}

// Error message
function errorFunctionAll(xhr, status, strErr) {
  $('#infoSearch').html('<p>An error has occurred</p>');
}