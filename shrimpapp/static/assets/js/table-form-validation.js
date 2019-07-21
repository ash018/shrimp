/**
 * Created by shakil.ahammad on 7/9/2019.
 */

function writeUpdatedDataModalToCell(){
    $("#myModal").on("click", "button#ModalPkgMatUpdate", function () {
        var tableId = $('#myModal input#TableIdForModal').val();
        var rowIndex = $('#myModal input#TableRowIdxForModal').val();
        var cellIndex = $('#myModal input#TableCellIdxForModal').val();
        var pakMatNQnt = '';
        var userPkgData = '';
        $('#PakMatCheckTable input[type=checkbox]:checked').each(function () {
            var row = $(this).closest("tr")[0];
            var pkgCount = '0';
            if (row.cells[1].children[0].value != '') {
                pkgCount = row.cells[1].children[0].value;
            }
            userPkgData += $(this).val() + '!' + pkgCount + '-';
        });

        var pkgHtml = '<input name="' + tableId.split("_")[1] + '" type="hidden" class="PkgMatInput" value="' + userPkgData + '"/>';
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).css('background-color', '#DDA0DD');
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).find('input.PkgMatInput').remove();
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).append(pkgHtml);
        $('#myModal').modal('hide');
    });
}

function writeDataModalToCell() {
    $("#myModal").on("click", "button#PkgMatSave", function () {
        var tableId = $('#myModal input#TableIdForModal').val();
        var rowIndex = $('#myModal input#TableRowIdxForModal').val();
        var cellIndex = $('#myModal input#TableCellIdxForModal').val();
        var pakMatNQnt = '';
        var userPkgData = '';
        $('#PakMatCheckTable input[type=checkbox]:checked').each(function () {
            var row = $(this).closest("tr")[0];
            var pkgCount = '0';
            if (row.cells[1].children[0].value != '') {
                pkgCount = row.cells[1].children[0].value;
            }
            userPkgData += $(this).val() + '!' + pkgCount + '-';
        });

        var pkgHtml = '<input name="' + tableId.split("_")[1] + '" type="hidden" class="PkgMatInput" value="' + userPkgData + '"/>';
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).css('background-color', '#DDA0DD');
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).find('input.PkgMatInput').remove();
        $('#' + tableId + ' tbody tr').eq(rowIndex).find('td').eq(cellIndex).append(pkgHtml);
        $('#myModal').modal('hide');
    });
}

function pkgMatModal(baseurl) {
    $("#add_prod_tab").on("click", "input.PkgMaterial", function () {
        var pItem = $(this).attr('data');

        var row = $(this).closest("tr").index();
        var tableId = $(this).closest("table").attr("id");
        var cell = $(this).closest("td").index();

        var pkgMat = $('#' + tableId + ' tbody tr').eq(row).find('td').eq(cell).find('input.PkgMatInput').val();

        $('#TableIdForModal').val(tableId);
        $('#TableRowIdxForModal').val(row);
        $('#TableCellIdxForModal').val(cell);

        $('#myModal').modal('show');
        $('#myModalLabel').empty();
        $('#PkgMaterailAdd').empty();
        $.ajax({
            url: baseurl,
            type: "GET",
            data: "ProdItem=" + pItem + "&PkgMat=" + pkgMat + "&csrfmiddlewaretoken=" + csrftoken,
            cache: false,
            dataType: 'json',
            success: function (data) {
                var response = $.parseJSON(JSON.stringify(data));
                var prodItem = $.parseJSON(JSON.stringify(response.ProdItem));
                var html = $.parseJSON(JSON.stringify(response.html));
                $('#myModalLabel').html("Package Material For " + prodItem);
                $('#PkgMaterailAdd').append(html);
            }
        });
    });
}

function pkgMatUpdateModal(baseurl) {
    $("#add_prod_tab").on("click", "input.PkgMatUpdate", function () {
        var pDetailId = $(this).attr('data');

        var row = $(this).closest("tr").index();
        var tableId = $(this).closest("table").attr("id");
        var cell = $(this).closest("td").index();

        var pkgMat = $('#' + tableId + ' tbody tr').eq(row).find('td').eq(cell).find('input.PkgMatInput').val();
        if(pkgMat === undefined){
            pkgMat = "XXX";
        }

        $('#TableIdForModal').val(tableId);
        $('#TableRowIdxForModal').val(row);
        $('#TableCellIdxForModal').val(cell);

        $('#myModal').modal('show');
        $('#myModalLabel').empty();
        $('#PkgMaterailAdd').empty();
        $.ajax({
            url: baseurl,
            type: "GET",
            data: "ProdDetailId=" + pDetailId+"&PkgMat="+pkgMat+"&csrfmiddlewaretoken=" + csrftoken,
            cache: false,
            dataType: 'json',
            success: function (data) {
                var response = $.parseJSON(JSON.stringify(data));
                var prodItem = $.parseJSON(JSON.stringify(response.ProdItem));
                var html = $.parseJSON(JSON.stringify(response.html));
                $('#myModalLabel').html("Package Material For " + prodItem);
                $('#PkgMaterailAdd').append(html);
            }
        });
    });
}


 //$('#SaveButtonProduction').prop('disabled', true);
//$('#SaveButtonProduction').prop('disabled', false);

function divTableProducItemCheck() {
     var selectItemHOSO = new Array();
     var selectItemPDTO = new Array();
     var selectItemPnD = new Array();
     var selectItemHLSO = new Array();
     var selectItemHLSO_non_treated = new Array();
     var selectItemEZP = new Array();
     var selectItemDeep_Cut = new Array();
     var selectItemCPDTO = new Array();
     var selectItemCPnD = new Array();
     var selectItemPD = new Array();

     var tRowsHOSO = $('#AddProdTo_HOSO tbody tr').length;
     var tRowsPDTO = $('#AddProdTo_PDTO tbody tr').length;
     var tRowsPnD = $('#AddProdTo_PnD tbody tr').length;
     var tRowsHLSO = $('#AddProdTo_HLSO tbody tr').length;
     var tRowsHLSO_non_treated = $('#AddProdTo_HLSO-non-treated tbody tr').length;
     var tRowsEZP = $('#AddProdTo_EZP tbody tr').length;
     var tRowsDeep_Cut = $('#AddProdTo_Deep-Cut tbody tr').length;
     var tRowsCPDTO = $('#AddProdTo_CPDTO tbody tr').length;
     var tRowsCPnD = $('#AddProdTo_CPnD tbody tr').length;
     var tRowsPD = $('#AddProdTo_PD tbody tr').length;

     $('#AddProdTo_HOSO .ShrimPItem').each(function (index, item) {
        selectItemHOSO.push(item.value);
     });

     $('#AddProdTo_PDTO .ShrimPItem').each(function (index, item) {
            selectItemPDTO.push(item.value);
     });

      $('#AddProdTo_PnD .ShrimPItem').each(function (index, item) {
        selectItemPnD.push(item.value);
     });

     $('#AddProdTo_HLSO .ShrimPItem').each(function (index, item) {
            selectItemHLSO.push(item.value);
     });

      $('#AddProdTo_HLSO-non-treated .ShrimPItem').each(function (index, item) {
        selectItemHLSO_non_treated.push(item.value);
     });

     $('#AddProdTo_EZP .ShrimPItem').each(function (index, item) {
            selectItemEZP.push(item.value);
     });

     $('#AddProdTo_Deep-Cut .ShrimPItem').each(function (index, item) {
            selectItemDeep_Cut.push(item.value);
     });

     $('#AddProdTo_CPDTO .ShrimPItem').each(function (index, item) {
        selectItemCPDTO.push(item.value);
     });

     $('#AddProdTo_CPnD .ShrimPItem').each(function (index, item) {
            selectItemCPnD.push(item.value);
     });

     $('#AddProdTo_PD .ShrimPItem').each(function (index, item) {
        selectItemPD.push(item.value);
     });

     if((selectItemHOSO.allValuesSame() && tRowsHOSO > 1)  ||
         (selectItemPDTO.allValuesSame() && tRowsPDTO > 1) ||
         (selectItemPnD.allValuesSame() && tRowsPnD > 1)   ||
         (selectItemHLSO.allValuesSame() && tRowsHLSO > 1) ||
         (selectItemHLSO_non_treated.allValuesSame() && tRowsHLSO_non_treated > 1) ||
         (selectItemEZP.allValuesSame() && tRowsEZP > 1) ||
         (selectItemDeep_Cut.allValuesSame() && tRowsDeep_Cut > 1) ||
         (selectItemCPDTO.allValuesSame() && tRowsCPDTO > 1) ||
         (selectItemCPnD.allValuesSame() && tRowsCPnD > 1) ||
         (selectItemPD.allValuesSame() && tRowsPD > 1)){
         return 1;
     }
     else{
         return 0;
     }
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