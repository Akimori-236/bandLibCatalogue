$(document).ready(function () {
    $("form").submit(function (event) {
        var formData = {
            // selectors
            catalogueNo: $("#catalogueNoID").val(),
            title: $("#titleID").val(),
            composer: $("#composerID").val(),
            arranger: $("#arrangerID").val(),
            publisher: $("#publisherID").val(),
            feat: $("#featID").val(),
            ensemble: $("#ensembleID").val(),
            parts: $("#partsID").val(),
            remarks: $("#remarksID").val(),
        };

        // if (confirm('Confirm insert' + title  + '?')) {
            $.ajax({
                type: "POST",
                url: "https://elitelib22.pythonanywhere.com/newmusic/",
                data: formData,
                dataType: "json",
                encode: true,
            }).done(function (data) {
                console.log(data);
            });
        // }

        event.preventDefault();
    });
});