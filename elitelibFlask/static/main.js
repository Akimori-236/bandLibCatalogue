function capitalise(str) {
    let cap1st = str.charAt(0).toUpperCase() + str.slice(1);
    return cap1st;
}

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
function populateEnsembleList() {
    var output = '<option selected disabled hidden>         </option>'
    for (let i=0; i < ensembleList.length; i++) {
        output += '<option value="'+(i+1)+'">'+ ensembleList[i] +'</option>'
    }
    $('#ensembleList').html(output)
}

// Categories
const categories = [['00', 'Non-Published'],
                    ['10', 'Wind Band'],
                    ['11', 'Wind Band (A5)'],
                    ['12', 'Ceremonial Music'],
                    ['13', 'Foreign Anthem'],
                    ['14', 'Wind Band Training'],
                    ['20', 'Flute'],
                    ['21', 'Oboe'],
                    ['22', 'Cor Anglais'],
                    ['23', 'Bassoon'],
                    ['24', 'Clarinet'],
                    ['25', 'Saxophone'],
                    ['30', 'Horn'],
                    ['31', 'Trumpet'],
                    ['32', 'Trombone'],
                    ['33', 'Euphonium'],
                    ['34', 'Tuba'],
                    ['40', 'Strings'],
                    ['41', 'Piano'],
                    ['42', 'Harp/Guitar'],
                    ['50', 'Percussion'],
                    ['60', 'Recorder'],
                    ['61', 'Vocal'],
                    ['70', 'Woodwind Ensemble'],
                    ['71', 'Brass Ensemble'],
                    ['72', 'Mixed Ensemble'],
                    ['73', 'Flexible Ensemble'],
                    ['74', 'Big Band'],
                    ['80', 'Reference'],
                    ['81', 'Theory Papers G5'],
                    ['82', 'Theory Papers G6'],
                    ['83', 'Theory Papers G7'],
                    ['84', 'Theory Papers G8'],
                    ['85', 'Theory Material'],
                    ['86', 'Aural Material'],
                    ['90', 'Wind Band/Orch Disc'],
                    ['91', 'Instrument/Chamber Disc'],
                    ['92', 'Miscellaneous/Archive Disc'],
                    ['93', 'Wind Band Training Disc'],
                    ['94', 'Marching Band Disc']
];
function populateCategoryList() {
    var output = '<option selected disabled hidden>             </option>'
    for (let i=0; i < categories.length; i++) {
        output += '<option value="'+categories[i][0]+'">'+ categories[i][1] +'</option>'
    }
    $('#categoryList').html(output)
}

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
    var categoryID = $('#categoryList').val();
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


function getMusicByEnsembleType(ensemble) {
    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/ensemble/' + ensemble,
        type: 'GET',
        dataType: 'json',
        success: successDisplayTable,
        error: showErrorMsg,
    });
    return false;
}


function getMusicByCatNo() {
    //selectors
    var catNo = $('#catalogueNoID').val();
    var title = $('#titleID');
    var composer = $('#composerID');
    var arranger = $('#arrangerID');
    var publisher = $('#publisherID');
    var featInstru = $('#featID');
    var ensemble = $('#ensembleID');
    var parts = $('#partsID');
    var remarks = $('#remarksID');

    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/music/catno/' + catNo,
        type: 'GET',
        dataType: 'json',
        success: function(result) {
            console.log(result);
            title.val(result.Music[3]);
            composer.val(result.Music[4]);
            arranger.val(result.Music[5]);
            publisher.val(result.Music[6]);
            featInstru.val(result.Music[7]);
            ensemble.val(ensembleList[result.Music[8]-1]);
            parts.val(result.Music[9]);
            remarks.val(result.Music[10]);
            window.title = title.val();
        },
        error: showErrorMsg,
    });
    return false;
}



// Display all music in a table
function successDisplayTable(result) {
    $('#searchResults').html("");
    strHTMLcontent = "<a href='/print' class='btn btn-danger m-2'>Printable Version</a>" +
        "<table id='results' class='table table-bordered table-hover table-dark mx-2'>" +
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
            let composer = result.Music[index][4];
            if (typeof composer  == 'object' || composer  == '') {
                composer = '-';
            }
            let arranger = result.Music[index][5];
            if (typeof arranger == 'object' || arranger  == '') {
                arranger = '-';
            }
            let publisher = result.Music[index][6];
            if (typeof publisher == 'object' || publisher == '') {
                publisher = '-';
            }
            let featInstru = result.Music[index][7];
            if (typeof featInstru == 'object' || featInstru == '') {
                featInstru = '-';
            }
            let ensemble = ensembleList[Number(result.Music[index][8]) - 1];
            if (typeof ensemble == 'undefined' || typeof ensemble == 'object' || ensemble == '') {
                ensemble = '-'
            }
            let parts = result.Music[index][9];
            if (typeof parts == 'object' || parts == '') {
                parts = '-';
            }
            let remarks = result.Music[index][10];
            if (typeof remarks == 'object' || remarks == '') {
                remarks = '-';
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


// search Music
function searchMusic() {
    var strHTMLcontent = "";
    //selector
    var searchType = $('#searchselectID').val();
    var query = $('#searchtextboxID').val();
    console.log('Searching for: ' + query);

    $.ajax({
        url: 'http://elitelib22.pythonanywhere.com/search/'+ searchType +'?q=' + query,
        type: 'GET',
        dataType: 'json',
        success: successDisplayTable,
        error: showErrorMsg,
    });
    return false;
}



// about lol
function showAbout() {
  $('#searchResults').html('<div class="card bg-dark position-absolute top-50 start-50 translate-middle border border-danger rounded-3" style="width: 18rem;">' +
                            '<div class="card-body">' +
                            '<h5 class="card-title text-light text-center mb-3">About</h5>' +
                            '<p class="card-text text-light my-0"> Created by ME1-2 Ng Wee Seng in April-May 2022 </p>' +
                            '<br><br>' +
                            '<h6 class="card-subtitle mb-2 text-muted text-center">Band Digitalization Team 2022</h6>' +
                            '<p class="card-text text-light my-0"> ME2-2 Joe Tan </p>' +
                            '<p class="card-text text-light my-0"> ME1-2 Ng Wee Seng  </p>' +
                            '<p class="card-text text-light my-0"> ME1-2 Vignesh  </p>' +
                            '<p class="card-text text-light my-0"> ME1-2 Gerald Lim </p>' +
                            '<p class="card-text text-light my-0"> ME1-2 Kenneth Low  </p>' +
                            '</div>' +
                            '</div>'
                            );
}

// Error message
function showErrorMsg(xhr, status, strErr) {
  $('#searchResults').html('<div class="card bg-dark position-absolute top-50 start-50 translate-middle border border-danger rounded-3" style="width: 18rem;">' +
                            '<div class="card-body">' +
                            '<h5 class="card-title text-light text-center">'+ capitalise(status) +'</h5>' +
                            '<h6 class="card-subtitle mb-2 text-muted text-center">' + strErr + '</h6>' +
                            '<p class="card-text text-light text-center">Sorry ah, cannot find.</p>' +
                            '</div>' +
                            '</div>'
                            );
}


