/**
 * Created by shakil.ahammad on 7/9/2019.
 */

function divTableProducItemCheck(){
    var tableIds = $("#add_prod_tab table").map(function(i, table){
                    return table.id;
                }).get();

    // $("#ProductionType #AddProdTo_HOSO td.shrimpproductitem").each(function(index){
    //         console.log("----");
    //     });


    // var sel = $("#add_prod_tab table").map(function(i, table){
    //                 return table.id;
    //             }).get();



        $('#ProductionType').load('table #AddProdTo_HOSO', function () {
            //var s = $('#AddProdTo_HOSO .ShrimPItem option:selected').val();
            $('#AddProdTo_HOSO .ShrimPItem').each(function(index,item){
                console.log("---"+index+ "--"+item.value);
            });
            // $('#AddProdTo_HOSO').find('.ShrimPItem option:selected', function(){
            //     console.log("---"+$(this).val());
            // });


        });



    // $("this table #AddProdTo_HOSO").find("td.shrimpproductitem").each(function(){
    //         var  selectedVal = $(this ).find(":selected").val();
    //         //alert(selectedVal);
    //         console.log(selectedVal);
    //     });
    // $("#ProductionType #AddProdTo_HOSO td.shrimpproductitem").each(function(index){
    //         console.log("----");
    //     });


    // for(var k = 0; k<tableIds.length; k++){
    //     //$("#ProductionType "+tableIds[k]+" shrimp-product-item")
    //     $('#' +  tableIds[k]).find("td.shrimpproductitem").each(function(index){
    //         console.log("----");
    //     });
    //     console.log('#' +  tableIds[k]);
    //     // var selectedItem = $("#"+tableIds[k]+" td shrimpproductitem").map(function(i, spi){
    //     //             return spi.val();
    //     //         }).get();
    //     //console.log(selectedItem.join(', '));
    //      //console.log( tableIds[k]);
    // }
}
