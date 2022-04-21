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


// get total music count
var totalMusicCount = function () {
    var tmp = null;
    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/music/totalcount',
        type: "GET",
        dataType: 'json',
        async: false,
        global: false,
        'data': { 'request': "", 'target': 'arrange_url', 'method': 'method_target' },
        'success': function (data) {
            tmp = data;
        }
    });
    return tmp;
}();
totalMusicCount = totalMusicCount['TotalMusic'][0][0]
console.log(totalMusicCount)





// Show all sheet music
function getAllMusic() {

    var strHTMLcontent = ""; // insert search result

    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/music',
        type: 'GET',
        dataType: 'json',
        success: successDisplayTable,
        error: showErrorMsg,
    });

    return false;
}


// Show sheet music by page
// function getMusicByPage(page) {

//     var strHTMLcontent = ""; // insert search result

//     $.ajax({
//         url: 'http://elitelib22.pythonanywhere.com/music?page=' + String(page),
//         type: 'GET',
//         dataType: 'json',
//         success: successDisplayAdminTable,
//         error: showErrorMsg,
//     });

//     return false;
// }

// Display all music in a table
function successDisplayTable(result) {
    $('#searchResults').html("");
    strHTMLcontent = "<table id=\"results\" class='table table-bordered table-hover table-dark'>" +
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
        "</tr>" +
        "</thead>";

    var jObjects = result.Music
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
            let musicID = result.Music[index].musicID
            // console.log(result.Music[index])
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
            "<td>" + result.Music[index][10] + "</td>"; // [10] remarks
        }
    }
    else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#searchResults').html(strHTMLcontent);
}


// Display all music in a table WITH ADMIN Controls
function successDisplayAdminTable(result) {
    $('#searchResults').html("");
    strHTMLcontent = "<table id=\"results\" class='table table-bordered table-hover table-dark'>" +
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
            // console.log(result.Music[index])
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
            "<td>" + deleteBtn + "</td>";
        }
    }
    else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#searchResults').html(strHTMLcontent);

    //pagination test
    $('#pagination').html(displayPagination(totalMusicCount));
}


// Error message
function showErrorMsg(xhr, status, strErr) {
  $('#searchResults').html('<p>An error has occurred</p>');
}



// Delete music
function deleteMusicByID(musicID) {
    if (confirm("Confirm delete music?")) {
        $.ajax({
            url: 'http://elitelib22.pythonanywhere.com/music' + String(musicID),
            type: 'DELETE',
            dataType: 'json',
            success: getAllMusic,
            error: showErrorMsg,
        });
    } else {
        console.log("Cancelled deletion of movie no." + String(musicID));
    }
}





// PAGINATION
function displayPagination(totalMusic) {

    // Get current page from URL variable
    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    });
    // Get the value of "some_key" in eg "https://example.com/?some_key=some_value"
    let currentPage = Number(params.page); // "some_value"
    var prevPage = currentPage-1;
    var displayData = '';
    var lastPage = Math.ceil(totalMusic/10);

    // build the pagination display
    displayData += '<nav> <div class="btn-group" role="group">';
    displayData += '<button onclick="getMusicByPage(1)" type="button" class="btn btn-outline-primary me-3">First</button>';
    if (currentPage == 1) {
        displayData += '<button type="button" class="btn btn-outline-primary me-1" disabled><</button>';
    } else {
        displayData += '<button type="button" class="btn btn-outline-primary me-1"><</button>';
    }
    '<button type="button" class="btn btn-outline-primary me-1"><</button>';
    // getMusicByPage(page)
    //         <button type="button" class="btn btn-outline-primary me-1"><</button>
    //         <button type="button" class="btn btn-outline-danger">1</button>
    //         <button type="button" class="btn btn-outline-danger">2</button>
    //         <button type="button" class="btn btn-outline-danger">3</button>
    //         <button type="button" class="btn btn-outline-info ms-1">></button>
    //         <button type="button" class="btn btn-outline-info ms-3">Last</button>


    displayData += '</div> </nav>';
    return displayData;
}