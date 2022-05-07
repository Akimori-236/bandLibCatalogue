function categorySelected() {
    // build category part of catalogueNo
    window.selectedCat = $("#categoryList").val();
    $("#catalogueNoID").html(selectedCat);
    // unlock the other inputs
    $("#boxList").prop("disabled", false);
    $("#existingBoxID").prop("disabled", false);
    // disables itemNo if not WindBand Category
    if (selectedCat == 10 || selectedCat == 11) {
        $("#itemID").prop("disabled", false);
        $("#oversizedBoxID").prop("disabled", false);
    } else {
        $("#itemID").prop("disabled", true);
        $("#oversizedBoxID").prop('checked',false);
        $("#oversizedBoxID").prop("disabled", true);
        $("#itemList").html("<option selected disabled hidden>             </option>");
        $("#itemList").prop("disabled", true);
    }
    console.log("Selected Category: " + selectedCat);
    // GET current boxes
    $.ajax({
        url:
            "http://elitelib22.pythonanywhere.com/boxes/" + String(selectedCat),
        type: "GET",
        dataType: "json",
        success: populateAvailableBoxes,
        error: function () {
            $("#boxList").html("<option selected value=''> ERROR </option>");
        },
    });
    return false;
}

function populateAvailableBoxes(result) {
    window.boxItems = result.Boxes; // save result to prevent multiple requests
    window.boxes = []; // current normal boxes
    window.oversized = []; // current oversized boxes

    for (let i=0, b=window.boxItems; i < b.length; i++) {
        let x = b[i].slice(0, 4);
        if (isNaN(x)) {
            if (!(x in oversized)) {
                window.oversized.push(Number(x.slice(1, 4)));
            }
        } else if (!window.boxes.includes(Number(x))) {
            window.boxes.push(Number(x));
        }
    }
    console.log("Current Boxes:" + window.boxes);
    console.log("Current Oversized Boxes:" + window.oversized);
    toggleExistingOrOversized();
}

function boxSelected() {
    // ENABLE ITEM SELECT IF WIND BAND CATEGORY
    if (window.selectedCat == 10 || window.selectedCat == 11) {
        $("#itemList").prop("disabled", false);
    }
    var selectedBox = $("#boxList").val();
    window.boxDisplayText = "";
    // FORMAT BOX VALUE
    if ($("#oversizedBoxID").is(":checked")) {
        // IF USING OVERSIZED BOX (X + 3 DIGITS)
        boxDisplayText = "00" + selectedBox;
        boxDisplayText = boxDisplayText.slice(-3);
        boxDisplayText = "X" + boxDisplayText;
    } else if (window.selectedCat == 10 || window.selectedCat == 11) {
        // IF WIND BAND CATEGORY (4 DIGITS)
        boxDisplayText = "000" + selectedBox;
        boxDisplayText = boxDisplayText.slice(-4);
    } else {
        // OTHER CATEGORIES (3 DIGITS)
        boxDisplayText = "000" + selectedBox;
        boxDisplayText = boxDisplayText.slice(-3);
    }
    // DISPLAY CATALOGUE NO OF SELECTED BOX
    $("#catalogueNoID").html(window.selectedCat + "-" + boxDisplayText);

    var output = "<option selected disabled hidden>             </option>";
    if ($("#existingBoxID").is(":checked")) {
        // if selectedBox + 02 in boxes, option value 3
        for (let i=1, counter = 0; counter < 1; i++) {
            let boxItemNo = window.boxDisplayText + "-0" + i;
            if (!(window.boxItems.includes(boxItemNo))) {
                output += "<option value='"+ i + "'> "+ i +" </option>"
                counter += 1;
            }
        }
    } else {
        if (window.selectedCat == 10 || window.selectedCat == 11) {
            // ITEM 1 IF USING NEW BOX IN WIND BAND CATEGORY
            output += "<option value='1'> 1 </option>"
        }
    }

    console.log("Selected Box: " + selectedBox);
    $("#itemList").html(output);
}

function itemSelected() {
    var selectedItem = $("#itemList").val();
    window.itemDisplayText = "";
    // FORMAT ITEM VALUE
    if (window.selectedCat == 10 || window.selectedCat == 11) {
        // IF WIND BAND CATEGORY (4 DIGITS)
        itemDisplayText = "0" + selectedItem;
        itemDisplayText = itemDisplayText.slice(-2);
    }
    // DISPLAY CATALOGUE NO OF SELECTED BOX
    console.log("Selected Item: " + selectedItem);
    $("#catalogueNoID").html(
        window.selectedCat + "-" + window.boxDisplayText + "-" + window.itemDisplayText
    );
}


function toggleExistingOrOversized() {
    var output = "<option selected disabled hidden>             </option>";
    if ($("#oversizedBoxID").is(":checked")) {
        if (window.oversized.length != 0) {
            // SORT LIST IF LIST IS NOT EMPTY
            window.oversized.sort(function (a, b) {
                return a - b;
            });
        }
        let lastBox = window.oversized[window.oversized.length - 1];
        if ($("#existingBoxID").is(":checked")) {
            // USE EXISTING OVERSIZED BOX
            for (let i=0, b=window.oversized; i < b.length; i++) {
                output += "<option value='" + b[i] + "'>" + b[i] + "</option>";
            }
        } else {
            // CREATE NEW OVERSIZED BOX
            if (oversized.length === 0) {
                // IF THERE IS CURRENTLY NO OVERSIZED BOXES IN USE FOR THE CATEGORY
                output += "<option value='1'> 1 </option>";
            } else {
                for (let i=1, last=lastBox; i <= last + 1; i++) {
                    if (!window.oversized.includes(i)) {
                        output +=
                            "<option value='" + i + "'>" + i + "</option>";
                    }
                }
            }
        }
    } else {
        if (window.boxes.length != 0) {
            // SORT LIST IF LIST IS NOT EMPTY
            window.boxes.sort(function (a, b) {
                return a - b;
            });
        }
        let lastBox = window.boxes[window.boxes.length - 1];
        if ($("#existingBoxID").is(":checked")) {
            // USE EXISTING BOX
            for (let i=0, b=window.boxes; i < b.length; i++) {
                output += "<option value='" + b[i] + "'>" + b[i] + "</option>";
            }
        } else {
            // CREATE NEW BOX
            if (boxes.length === 0) {
                // IF THERE IS CURRENTLY NO BOXES IN USE FOR THE CATEGORY
                output += "<option value='1'> 1 </option>";
            } else {
                for (let i = 1, last = lastBox; i <= last + 1; i++) {
                    if (!window.boxes.includes(i)) {
                        output +=
                            "<option value='" + i + "'>" + i + "</option>";
                    }
                }
            }
        }
    }
    $("#boxList").html(output);
}

// Insert Music
function insertMusic() {
    let input = {
        'catalogueNo'   : (window.selectedCat + "-" + window.boxDisplayText + "-" + window.itemDisplayText),
        'categoryID'    : window.selectedCat,
        'title'         : $("#titleID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'composer'      : $("#composerID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'arranger'      : $("#arrangerID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'publisher'     : $("#publisherID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'featuredInstrument' : $("#featID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'ensembleID'    : $("#ensembleList").val(),
        'parts'         : $("#partsID").val().toUpperCase().replace(/\s+/g, " ").trim(),
        'remarks'       : $("#remarksID").val().toUpperCase().replace(/\s+/g, " ").trim()
    }
    if (confirm("Confirm insert '"+ $('#titleID').val() +"'?")) {
        $.ajax({
            url: 'http://elitelib22.pythonanywhere.com/newmusic',
            type: 'POST',
            dataType: 'json',
            data: input,
            success: showSuccessMsg(input['title']),
            error: showErrorMsg(input['title']),
        });
    } else {
        showCancelMsg(input['title']);
    }
    return false;
}

function showErrorMsg(title) {
    $('#msgbox').html("<p class='text-center mx-auto w-auto rounded-pill text-white bg-danger'>Error inserting '" + title + "'.</p>");
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    console.log("Error inserting '" + $('#titleID').val() + "'.");
}

function showSuccessMsg(title) {
    $('#msgbox').html("<p class='text-center mx-auto w-auto rounded-pill text-white bg-success'>Successfully inserted '" + title + "'.</p>");
    $("#insertMusicFormID")[0].reset();
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    console.log("Successful insertion of '" + $('#titleID').val() + "'.");
}

function showCancelMsg(title) {
    $('#msgbox').html("<p class='text-center mx-auto w-auto rounded-pill text-dark bg-info '>Cancelled insertion of '" + $('#titleID').val() + "'.</p>");
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    console.log("Cancelled insertion of '" + $('#titleID').val() + "'.");
}



// Delete music
function deleteMusicByCatNo() {
    if (confirm("Confirm delete " + window.title + "?")) {
        var catNo = $('#catalogueNoID').val();

        $.ajax({
            url: 'http://elitelib22.pythonanywhere.com/music/' + catNo,
            type: 'DELETE',
            dataType: 'json',
            success: function() {
                $('#msgbox').html('<p class="btn btn-outline-success">JS: Successfully deleted ' + window.title + '</p>')
            },
            error: showErrorMsg,
        });
    } else {
        console.log("Cancelled deletion of " + window.title);
    }
    return false;
}