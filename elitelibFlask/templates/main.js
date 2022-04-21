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

// Display all music in a table
function successFunctionAll(result) {
    $('#searchResults').html("");
    strHTMLcontent = "<table id=\"results\" class='table table-bordered table-dark'>" +
        "<thead class='thead-light'>" +
        "<tr>" +
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
        "</tr>" +
        "</thead>";

    var jObjects = result.Music
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
            let musicID = result.Music[index].musicID
            console.log(result.Music[index])
            strHTMLcontent += "<tr>"+
            // Data                                     // [0] musicID
            "<td>" + result.Music[index][1] + "</td>" + // [1] Catalogue Number [2] categoryID
            "<td>" + result.Music[index][3] + "</td>" + // [3] title
            "<td>" + result.Music[index][4] + "</td>" + // [4] composer
            "<td>" + result.Music[index][5] + "</td>" + // [5] arranger
            "<td>" + result.Music[index][6] + "</td>" + // [6] publisher
            "<td>" + result.Music[index][7] + "</td>" + // [7] featuredInstrument
            "<td>" + result.Music[index][8] + "</td>" + // [8] ensembleID               change ensembleID to ensemble
            "<td>" + result.Music[index][9] + "</td>" + // [9] parts
            "<td>" + result.Music[index][10] + "</td>" +// [10] remarks

            // delete button
            "<td>" + "<a href='#' class='btn btn-default btn-danger rounded-circle px-3' onclick='return deleteMovieByID("+musicID+")'>" + "X" +"</a>" + "</td>";
        }
    }
    else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#searchResults').html(strHTMLcontent);
}

// Error message
function errorFunctionAll(xhr, status, strErr) {
  $('#searchResults').html('<p>An error has occurred</p>');
}