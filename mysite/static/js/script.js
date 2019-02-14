$(document).ready( function () {
    //$('#table_id').DataTable();
    console.log("hello world 2");

    $('.team').on('click', function(e) {
    	 if (e.target !== this)
    		return;
    	$(this).find('.url').toggleClass('hide');
    	$(this).find('.save').toggleClass('hide');
    });

});


function setActive(id){
	$(".nav-item").removeClass("active");
	$("#"+id).addClass("active");
}
