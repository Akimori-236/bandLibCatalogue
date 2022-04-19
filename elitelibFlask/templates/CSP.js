fetch('http://localhost:5000')
    .then(function (response) {
        if (response.status === 200) console.log('%cConnected to backend!', 'color: green');
        return response.json();
    })
    .then(function (json) {
        console.log(json);
    })
    .catch(function (error) {
        console.error('Failed to connect to backend! Error: ', error);
    });

// get genres
var allGenres = function () {
    var tmp = null;
    $.ajax({
        url: 'http://localhost:5000/genres',
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
allGenres = allGenres['Genres']
//console.log(allGenres)

// Show all active screening movies
function getAllActiveMovies() {

    var strHTMLcontent = ""; // insert search result

    $.ajax({
        url: 'http://localhost:5000/movies',
        type: 'GET',
        dataType: 'json',
        success: successFunctionAll,
        error: errorFunctionAll,
    });

    return false;
}

// Delete movie
function deleteMovieByID(movieID) {
    if (confirm("Confirm delete movie?")) {
        $.ajax({
            url: 'http://localhost:5000/movies/' + String(movieID),
            type: 'DELETE',
            dataType: 'json',
            success: getAllActiveMovies,
            error: errorFunctionAll,
        });
    } else {
        console.log("Cancelled deletion of movie no." + String(movieID));
    }
}

// Update movie genre
function updateMovieByID(movieID, newGenreID) {
    var jsonOutput = {'genreID' : Number(newGenreID)};
    console.log(jsonOutput)
    $.ajax({
        url: 'http://localhost:5000/movies/' + String(movieID),
        type: 'PUT',
        dataType: 'json',
        data: jsonOutput,
        success: getAllActiveMovies,
        error: errorFunctionAll,
    });
    return false;
}

// Sort movie
function sortByReleaseDate() {
    var strHTMLcontent = "";
    $.ajax({
        url: 'http://localhost:5000/movies/sort',
        type: 'GET',
        dataType: 'json',
        success: successFunctionAll,
        error: errorFunctionAll,
    });
    return false;
}

// change genre button
function changeGenreButton(movieID) {
    var newGenreID = Number($("#movie"+movieID).val());
    //console.log(newGenreID);
    return updateMovieByID(movieID, newGenreID);
}

// Display all movies in a table
function successFunctionAll(result) {
    $('#infoSearch').html("");
    strHTMLcontent = "<table id=\"results\"><tr>" + 
        "<th>Movie Name</th>" +  
        "<th>Description</th>" + 
        "<th>Genre</th>" + 
        "<th>Release Date</th>" + 
        "<th>Delete</th>" + 
        "<th>Update Genre</th>" +
        "</tr>";
  
    var jObjects = result.Movies
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
            let movID = result.Movies[index].movieID

            strHTMLcontent += "<tr>"+
            "<td>" + result.Movies[index].movieName + "</td>" +
            "<td>" + result.Movies[index].movieDescription + "</td>" +
            "<td>" + result.Movies[index].genreName + "</td>" +
            "<td>" + result.Movies[index].releaseDate + "</td>" +
            
            // delete button
            "<td>" + "<a href='#' class='btn btn-default btn-danger rounded-circle px-3' onclick='return deleteMovieByID("+movID+")'>" + "X" +"</a>" + "</td>" +
            
            // genre drop down list
            "<td>" + "<form><select id='movie" + movID + "'><option> Select a Genre</option>"
            for (let i = 0; i < allGenres.length; i++) {
                strHTMLcontent += "<option value='" + allGenres[i]["genreID"] + "'>" + allGenres[i]['genreName'] + "</option>";
            }
        strHTMLcontent += "</select><input class='mx-1' type='submit' value='Change' onclick='return changeGenreButton("+movID+")'></form>" +
            "</td>" + "</tr>";
        }
    }else {
        strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#infoSearch').html(strHTMLcontent);
}

// Error message 
function errorFunctionAll(xhr, status, strErr) {
  $('#infoSearch').html('<p>An error has occurred</p>');
}

//Search for movie based on substring of movie name
function getMoviesBySubstring() {

    var strHTMLcontent = ""; // insert search result

    $.ajax({
        url: 'http://localhost:5000/search/movies?name=' + $('input#txtBoxSearch').val(),
        type: 'GET',
        dataType: 'json',
        success: successFunctionSubstr,
        error: errorFunctionSubstr,
    });

    return false;
}

// Display search result in a table
function successFunctionSubstr(result) {
    
    $('#infoSearch').html("");
    strHTMLcontent = "<table id=\"results\"><tr>" +
        "<th>Movie Name</th>" +
        "<th>Description</th>" +
        "<th>Genre</th>" +
        "<th>Release Date</th>" +
        "<th>Delete</th>" +
        "<th>Update Genre</th>" +
        "</tr>";
    var jObjects = result.Movies
    if (jObjects.length > 0) { // Check if there are any results:
        for (var index in jObjects) {
        strHTMLcontent += "<tr>"+
            "<td>" + result.Movies[index].movieName + "</td>" +
            "<td>" + result.Movies[index].movieDescription + "</td>" +
            "<td>" + result.Movies[index].genreName + "</td>" +
            "<td>" + result.Movies[index].releaseDate + "</td>" +
            // delete button
            "<td>" + "<a href='#' class='btn btn-default btn-danger rounded-circle px-3' onclick='return deleteMovieByID("+result.Movies[index].movieID+")'>" + "X" +"</a>" + "</td>" +
            // genre drop down list
            "<td>" + "<form><select id='movie"+result.Movies[index].movieID+"'><option> Select a Genre</option>"
            for (let i = 0; i < allGenres.length; i++) {
                strHTMLcontent += "<option value='" + allGenres[i]["genreID"] + "'>" + allGenres[i]['genreName'] + "</option>";
            }
        strHTMLcontent += "</select><input class='mx-1' type='submit' value='Change' onclick='return changeGenreButton("+result.Movies[index].movieID+")'></form>" + "</td>" +
            "</tr>";
        }
    }else {
    strHTMLcontent += "<tr><td>No results found</td></tr>";
    }
    strHTMLcontent += "</table>";
    $('#infoSearch').html(strHTMLcontent);
}

function errorFunctionSubstr(xhr, status, strErr) {
  $('#infoSearch').html('<p>An error has occurred</p>');
}
console.log(allGenres)