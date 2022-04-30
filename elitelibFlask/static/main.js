// ENSEMBLE TYPES
const ensembleList = [
    "Concert Band",
    "Marching Band",
    "Solo",
    "Ensemble",
    "Big Band",
    "Study",
    "Reference",
    "Others"
];

// DELETE BUTTON
const deleteBtn = `<button type="button" class="btn btn-outline-danger">
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="bi bi-trash3-fill"
        viewBox="0 0 16 16"
    >
        <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"></path>
    </svg>
    <span class="visually-hidden">Button</span>
</button>`;



// Show music by category
function selectCategory() {
    var categoryID = $('#category').val();
    var strHTMLcontent = ""; // insert search result
    console.log("Getting Category:" + String(categoryID));
    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/category/' + String(categoryID),
        type: 'GET',
        dataType: 'json',
        success: successDisplayTable,
        error: showErrorMsg,
    });

    return false;
}



// // get total music count
// function getMusicCount() {
//     var musicCounter = 0;
//     var paginationHTML = "";

//     $.ajax({
//         url: 'http://elitelib22.pythonanywhere.com/music/totalcount/',
//         type: "GET",
//         dataType: 'json',
//         success: displayPagination,
//         error: showErrorMsg,
//     })

//     return false;
// }



// Show all sheet music
function getAllMusic() {

    var strHTMLcontent = ""; // insert search result

    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/music/',
        type: 'GET',
        dataType: 'json',
        success: successDisplayTable,
        error: showErrorMsg,
    });

    return false;
}




// Display all music in a table
function successDisplayTable(result) {
    $('#searchResults').html("");
    strHTMLcontent = "<a href='/print' class='float-end btn btn-danger mb-3'>Printable Version</a>" +
        "<table id='results' class='table table-bordered table-hover table-dark'>" +
        "<thead class='thead-light'>" +
        "<tr class='text-danger'>" +
        "<th>Catalogue Number</th>" +
        "<th>Title</th>" +
        "<th>Composer</th>" +
        "<th>Arranger</th>" +
        "<th>Publisher</th>" +
        "<th>Featured Instrument</th>" +
        "<th>Ensemble Type</th>" +
        "<th>Parts</th>" +
        "<th>Remarks</th>" +
        "</tr>" +
        "</thead>";

    var jObjects = result.Music
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
            // Variables of each row
            let musicID = result.Music[index][0];
            let catalogueNo = result.Music[index][1];
            let catID = result.Music[index][2];
            let title = result.Music[index][3];
            let composer = '-';
            if (typeof result.Music[index][4]  != 'object') {
                composer = result.Music[index][4]
            }
            let arranger = '-';
            if (typeof result.Music[index][5] != 'object') {
                arranger = result.Music[index][5]
            }
            let publisher = '-';
            if (typeof result.Music[index][6] != 'object') {
                publisher = result.Music[index][6]
            }
            let featInstru = '-';
            if (typeof result.Music[index][7] != 'object') {
                featInstru = result.Music[index][7]
            }
            let ensemble = ensembleList[Number(result.Music[index][8]) - 1];
            if (typeof ensemble == 'undefined') {
                ensemble = '-'
            }
            let parts = '-';
            if (typeof result.Music[index][9] != 'object') {
                parts = result.Music[index][9]
            }
            let remarks = '-';
            if (typeof result.Music[index][10] != 'object') {
                remarks = result.Music[index][10]
            }

            strHTMLcontent += "<tr>"+
            // Data
            "<td>" + catalogueNo + "</td>" +
            "<td>" + title + "</td>" +
            "<td>" + composer + "</td>" +
            "<td>" + arranger + "</td>" +
            "<td>" + publisher + "</td>" +
            "<td>" + featInstru + "</td>" +
            "<td>" + ensemble + "</td>" +
            "<td>" + parts + "</td>" +
            "<td>" + remarks + "</td>";
        }
    }
    else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#searchResults').html(strHTMLcontent);
}



// Delete music
function deleteMusicByID(musicID) {
    if (confirm("Confirm delete music?")) {
        $.ajax({
            url: 'http://elitelib22.pythonanywhere.com/music/' + String(musicID),
            type: 'DELETE',
            dataType: 'json',
            success: getAllMusic,
            error: showErrorMsg,
        });
    } else {
        console.log("Cancelled deletion of movie no." + String(musicID));
    }
}



// Error message
function showErrorMsg(xhr, status, strErr) {
  $('#searchResults').html('<div class="card bg-dark position-absolute top-50 start-50 translate-middle border border-danger rounded-3" style="width: 18rem;">' +
                            '<div class="card-body">' +
                            '<h5 class="card-title text-light text-center">Error 404</h5>' +
                            '<h6 class="card-subtitle mb-2 text-muted text-center">Sorry ah, cannot find.</h6>' +
                            '<p class="card-text text-light">Aiyo what did you do, double check your inputs and try again.</p>' +
                            '</div>' +
                            '</div>'
                            );
}


