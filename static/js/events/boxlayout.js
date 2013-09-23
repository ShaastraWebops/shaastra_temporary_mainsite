/* ---------- EVENT GROUPS -------- */
//
function show_event_group(el) {
    el = $(el);
    item = el.parent();
    
    if (item.hasClass("event_item") || el.hasClass("event_item")) {
        if( el.hasClass("event_item") )
            item = el;
        // Item is the div that is required.
        
        $(".main_event_item").addClass("event_item"); // tell main_event it has data to show
        $(".main_event_item > div > div").hide();
        $(".main_event_item > div > div.title").show(); // Show the title for the boxes.
        $( '.main_event_item.event_item > div' ).show().removeClass( 'expand' ); // Tell the section that it is small.
        
        // Clean up main event

        // make other events smaller
        $(".event_items_div").addClass("offset2");
        $(".event_items_div .event_item").removeClass("span3");
        $(".event_items_div .event_item").addClass("span1");
    }
};

// A function to bring a person from the event main page to the event group page
function hide_event_group () {
    var main_event = $('.main_event_item'),
        events = $('.event_items_div .event_item');
        
    $(".main_event_item").removeClass("event_item"); // tell main_event it has data to show
    $(".main_event_item > div > div").hide();
    $(".main_event_item.event_item > div").hide().removeClass( 'expand' ); // Tell the section that it is small.
    
    // make other events bigger
    $(".event_items_div").removeClass("offset2");
    $(".event_items_div .event_item").removeClass("span1");
    $(".event_items_div .event_item").addClass("span3");
}


/* ---------- Shows the page which has list of pages for an event -------- */
function show_event(me) {
    var $el = $( '.main_event_item.event_item' ),
        $sections = $el.children( 'div' ),
        $section = $(me).parent();
        
    // expand the clicked section and hide the others
    $sections.hide();
    $section.show();
    $sections.removeClass( 'expand' );
    $section.addClass( 'expand' );
    $section.children("div").hide();
    $($section.children("div").get(1)).show();
    
};

// A function to bring a person from the event main page to the event group page
function hide_event () {
    var $el = $( '.main_event_item.event_item' ),
        $sections = $el.children( 'div' );
        
    $sections.show();
    $sections.removeClass( 'expand' );
    $sections.children("div").hide();
    $($sections.children("div").get(0)).show();
}

/* -------------------- EVENT PAGE ----------------- */

// A function to bring a person from the event main page to a specific page
function show_event_page(me) {
    var elem_number = $(me).parent().index(),
        $section = $($( '.main_event_item.event_item > div.expand > div' ).get(1));
        
    if ( elem_number != -1 ) {
        $section.children("div").hide(500);
        $($section.children("div").get(elem_number)).show(500); // +1 as title will also be there
        $(me).parent().parent().children("li").removeClass("active")
        $(me).parent().addClass("active")
    }
}

// A function to bring a person from the event-page to the event main page
function hide_event_page() {
    var $section = $( '.main_event_item.event_item > div.expand' );
    
    $section.children("div").hide();
    $($section.children("div").get(1)).show(); // +1 as title will also be there
    
}

