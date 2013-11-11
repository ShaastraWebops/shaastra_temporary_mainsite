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
        $(".main_lecture_item.lecture_item").html(item.children(".content").html()); // Tell the section that it is small.
            
        // Clean up main lecture

        // make other lectures smaller
        $(".lecture_items_div").addClass("offset");
        $(".lecture_items_div .lecture_item").removeClass("span4");
        $(".lecture_items_div .lecture_item").addClass("span2");
        $(".lecture_items_div .extra").show()
        $(".lecture_items_div .span1_5").hide()
        
        $(".lecture_item").removeClass("active")
        item.addClass("active")
        $(".back_button_lectures").show(100);
    }
}

function lecture_back() {

    $(".main_lecture_item").removeClass("lecture_item"); // tell main_lecture it has data to show
    $(".main_lecture_item > div > div").hide();
    $(".main_lecture_item > div").hide().removeClass( 'expand' ); // Tell the section that it is small.
    $(".main_lecture_item").html(""); // Tell the section that it is small.
    
    $(".lecture_items_div .span1_5").show();
    $(".lecture_items_div .extra").hide()
    $(".lecture_item").removeClass("active")
    $(".lecture_items_div .lecture_item").removeClass("span2");
    $(".lecture_items_div .lecture_item").addClass("span4");
    $(".lecture_carousel").show(500) 
    $(".back_button_lectures").hide(100);
}
