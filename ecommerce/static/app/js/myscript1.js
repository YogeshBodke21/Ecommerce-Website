$('.plus-cart').click( function(){
    var id = $(this).attr("pid");
    var eml = this.parentNode.children[2];
    console.log(id, eml)
    $.ajax({
        type:'GET',
        url:'/plusc',
        data : {
            prod_id : id
        },
        success:function(data){
            console.log("data=",data)
        }
    })
})