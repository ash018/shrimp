/**
 * Created by shakil.ahammad on 7/9/2019.
 */

function pkgMatModal(){
    $("#add_prod_tab").on("click", "input.PkgMaterial", function () {
        var pItem = $(this).attr('data');
        //console.log("This-" + pItem);
        $("#myModal").modal('show');
        //$("#myModal").dialog({minHeight: 300,minWidth:500});
        //$('#myModal').appendTo("body").modal('show');
    });
}

function divTableProducItemCheck (){
    $('#ProductionType').load('table #AddProdTo_HOSO', function () {
        var selectItem = new Array();
        $('#AddProdTo_HOSO .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HOSO tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_PDTO .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PDTO tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_PnD .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PnD tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_HLSO .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HLSO tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_HLSO-non-treated .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_HLSO-non-treated tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_EZP .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_EZP tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_Deep-Cut .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_Deep-Cut tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_CPDTO .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_CPDTO tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_CPnD .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_CPnD tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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
        $('#AddProdTo_PD .ShrimPItem').each(function(index,item){
            selectItem.push(item.value);
        });
        var tRows = $('#AddProdTo_PD tbody tr').length;
        if(selectItem.allValuesSame() && tRows > 1){

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

Array.prototype.allValuesSame = function() {
    for(var i = 1; i < this.length; i++)
    {
        if(this[i] !== this[0])
            return false;
    }
    return true;
}

function SaveButtonProduction(){
    $('#SaveButtonProduction').click(function(){
        $(this).attr('disabled','disabled');
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