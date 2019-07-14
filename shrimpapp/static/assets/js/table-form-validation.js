/**
 * Created by shakil.ahammad on 7/9/2019.
 */

function writeDataModalToCell(){
    $("#myModal").on("click", "button#PkgMatSave", function () {
        var tableId = $('#myModal input#TableIdForModal').val();
        var rowIndex = $('#myModal input#TableRowIdxForModal').val();
        var cellIndex = $('#myModal input#TableCellIdxForModal').val();
        var pakMatNQnt = '';
        var userPkgData = '';
        $('#PakMatCheckTable input[type=checkbox]:checked').each(function () {
                var row = $(this).closest("tr")[0];
                //console.log('------'+$(this).val()+'--'+row.cells[1].children[0].value);
                userPkgData += $(this).val() + '!' + row.cells[1].children[0].value+'-';
                //PakMatNQnt =

                // message += row.cells[1].innerHTML;
                // message += "   " + row.cells[2].innerHTML;
                // message += "   " + row.cells[3].innerHTML;
                // message += "\n";
            });

        var pkgHtml = '<input name="'+tableId.split("_")[1]+'" type="hidden" class="PkgMatInput" value="'+userPkgData+'"/>';
        $('#'+tableId+' tbody tr').eq(rowIndex).find('td').eq(cellIndex).css('background-color', '#DDA0DD');
        $('#'+tableId+' tbody tr').eq(rowIndex).find('td').eq(cellIndex).find('input.PkgMatInput').remove();
        $('#'+tableId+' tbody tr').eq(rowIndex).find('td').eq(cellIndex).append(pkgHtml);
        $('#myModal').modal('hide');

    });
}


function pkgMatModal(baseurl) {
    $("#add_prod_tab").on("click", "input.PkgMaterial", function () {
        var pItem = $(this).attr('data');

        var row = $(this).closest("tr").index();
        var tableId = $(this).closest("table").attr("id");
        var cell = $(this).closest("td").index();

        var pkgMat = $('#'+tableId+' tbody tr').eq(row).find('td').eq(cell).find('input.PkgMatInput').val();

        console.log("--this--" + pkgMat);

        $('#TableIdForModal').val(tableId);
        $('#TableRowIdxForModal').val(row);
        $('#TableCellIdxForModal').val(cell);

        $('#myModal').modal('show');
        $('#myModalLabel').empty();
        $('#PkgMaterailAdd').empty();
        $.ajax({
            url: baseurl,
            type: "GET",
            data: "ProdItem="+pItem+"&PkgMat="+pkgMat+"&csrfmiddlewaretoken=" + csrftoken,
            cache: false,
            dataType: 'json',
            success: function (data) {
                var response = $.parseJSON(JSON.stringify(data));
                var prodItem = $.parseJSON(JSON.stringify(response.ProdItem));
                var html = $.parseJSON(JSON.stringify(response.html));
                $('#myModalLabel').html("Package Material For "+ prodItem);
                $('#PkgMaterailAdd').append(html);
            }
        });
    });
}

function divTableProducItemCheck() {
    $('#ProductionType').load('table #AddProdTo_HOSO', function () {
        var selectItem = new Array();
        $('#AddProdTo_HOSO .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HOSO tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_PDTO', function () {
        var selectItem = new Array();
        $('#AddProdTo_PDTO .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PDTO tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_PnD', function () {
        var selectItem = new Array();
        $('#AddProdTo_PnD .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PnD tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_HLSO', function () {
        var selectItem = new Array();
        $('#AddProdTo_HLSO .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HLSO tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_HLSO-non-treated', function () {
        var selectItem = new Array();
        $('#AddProdTo_HLSO-non-treated .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HLSO-non-treated tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_EZP', function () {
        var selectItem = new Array();
        $('#AddProdTo_EZP .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_EZP tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_Deep-Cut', function () {
        var selectItem = new Array();
        $('#AddProdTo_Deep-Cut .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_Deep-Cut tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_CPDTO', function () {
        var selectItem = new Array();
        $('#AddProdTo_CPDTO .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_CPDTO tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_CPnD', function () {
        var selectItem = new Array();
        $('#AddProdTo_CPnD .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_CPnD tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });

    $('#ProductionType').load('table #AddProdTo_PD', function () {
        var selectItem = new Array();
        $('#AddProdTo_PD .ShrimPItem').each(function (index, item) {
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PD tbody tr').length;
        if (selectItem.allValuesSame() && tRows > 1) {

            sweetAlert({
                title: "This Item has already exist in this page.",
                text: "Please find the specific Table and add row. Thank You. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "DISMISS"
            });
        }
    });
}

Array.prototype.allValuesSame = function () {
    for (var i = 1; i < this.length; i++) {
        if (this[i] !== this[0])
            return false;
    }
    return true;
}

function SaveButtonProduction() {
    $('#SaveButtonProduction').click(function () {
        $(this).attr('disabled', 'disabled');
        sweetAlert({
            title: "This Item has already exist in this page.",
            text: "Please find the specific Table and add row. Thank You. ",
            type: "warning",
            showCancelButton: true,
            confirmButtonText: "DISMISS"
        });

        return false;
    });
}