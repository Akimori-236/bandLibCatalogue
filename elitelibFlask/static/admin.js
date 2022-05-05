function categorySelected() {
    // empty box and item selectors if category changed?
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
    window.boxes = [];
    window.oversized = [];
    for (let i = 0, b = window.boxItems; i < b.length; i++) {
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
    // unlock the other inputs
    $("#itemList").prop("disabled", false);
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
    if (
        (window.selectedCat == 10 || window.selectedCat == 11) && !$("#existingBoxID").is(":checked")) {
        // ITEM 1 IF USING NEW BOX IN WIND BAND CATEGORY
        output += "<option value='1'> 1 </option>"
    }
    // make list of items
    var items = [];
    for (let i=0; l=window.boxItems.length; i < l; i++) {
    //     if (isNaN(window.boxNo)) {
    //         if (boxItems[i].includes(window.boxNo)) {

    //         }
    //     } else {

    //     }
    }
    // for (let i=0, t=items; i < t.length; i++) {
    // output += '<option value="'+ result.Boxes[i] +'">'+ result.Boxes[i] +'</option>';
    // }
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
        window.selectedCat + "-" + boxDisplayText + "-" + itemDisplayText
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
