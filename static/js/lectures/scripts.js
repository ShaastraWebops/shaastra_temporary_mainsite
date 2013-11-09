function show_lecture(el) {
    el = $(el)
    parent = el.parent()
    item = parent
    
    if (item.hasClass("lecture_item") || el.hasClass("lecture_item")) {
        if( el.hasClass("lecture_item") )
            item = el;
        // Item is the div that is required.
        console.log(item)
        console.log(item.children("div.content").html()   )
        $(".main_lecture_item").addClass("lecture_item"); // tell main_lecture it has data to show
        $(".main_lecture_item.lecture_item").show().removeClass( 'expand' ); // Tell the section that it is small.
        $(".main_lecture_item.lecture_item").html(item.children(".content").html()); // Tell the section that it is small.
            
        // Clean up main lecture

        // make other lectures smaller
        $(".lecture_items_div").addClass("offset2");
        $(".lecture_items_div .lecture_item").removeClass("span3");
        $(".lecture_items_div .lecture_item").addClass("span1");
    }
}

function lecture_back() {

    $(".main_lecture_item").removeClass("lecture_item"); // tell main_lecture it has data to show
    $(".main_lecture_item > div > div").hide();
    $(".main_lecture_item.lecture_item > div").hide().removeClass( 'expand' ); // Tell the section that it is small.
    
    $(".lecture_carousel").show(500) 
}
