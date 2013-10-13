/* ---------- GET DATA -------- */
function boxlayout_init(){
    Dajaxice.frontend.show_events_list(process_json);
}

/* ---------- JSON PROCESSING -------- */
var json_content;

function process_json(json_data){
    json_content = json_data;//JSON.stringify(json_data);
}

function populate_event_group(category_name, dest){
    /*get the category name as stored in json file: underscores replaced with spaces and first letter capital for all words*/
    category_name = category_name.replace(/_/g, " ");
    str_array = category_name.split(/([_\W])/); // split based on spaces
    category_name = "";
    for(var i=0; i<str_array.length; i++){
        if(str_array[i] == "design"){
            category_name = "Design and build";
            break;
        }
        else{
            category_name += str_array[i].charAt(0).toUpperCase() + str_array[i].slice(1);
        }
    }
    
    
    /*populate the category with events*/
    event_list = json_content[category_name];
    dest.html(""); // make the dest empty to fill the events belonging to the given category
    
    $(".main_event_item.event_item").removeClass("rows_0") // gen
    $(".main_event_item.event_item").removeClass("rows_1")
    $(".main_event_item.event_item").removeClass("rows_2")
    $(".main_event_item.event_item").removeClass("rows_3")
    $(".main_event_item.event_item").addClass("rows_" + ( 1 + Math.floor(event_list.length/4) ))
    
    for (var i in event_list){
        if ( i == Math.floor(event_list.length/4)*4 ){ //provide proper span to center the 5th, 10th, ... element groups
            
            var left_over = event_list.length - Math.floor(event_list.length/4)*4,
                done = Math.floor(event_list.length/4)*4;
            span_amount = ( 12 - 3*left_over )/2;
            //console.log(span_amount)
            span_amount = span_amount.toString().replace(/\./g, "_");
            dest.append("<div class='span"+span_amount+"' style='opacity:0; z-index:-99;'></div>");
        }
        
        onclick_handler = "show_event(document.getElementById('event_no_" +event_list[i].pk+"_click'));" + "Dajaxice.events.show_event(Dajax.process,{'event_pk':'"+event_list[i].pk+"','event_name':'"+event_list[i].title.replace(/ /g, "~")+"','event_type':'"+event_list[i].event_type+"'});";
        dest.append("<div class='span3' id='event_no_"+event_list[i].pk+"'>"+
                        "<div class='span12 title' onclick="+onclick_handler+"  id='event_no_"+event_list[i].pk+"_click'><span><h3>"+event_list[i].title+"</h3></span><!--<br /><span class='white dice' style='opacity : 0.4'></span>--></div>"+
                        "<div class='span12 event_content'></div>"+
                    "</div>");
    }
    /*setTimeout(function() {
        dest.find("div.title").css ( {
            'height' : dest.height() + "px",
            'line-height' : dest.height() + "px",
        } );
    }, 5000);*/
}

/* ---------- EVENT GROUPS -------- */
function show_event_group(el) {
    el = $(el);
    item = el.parent();
    
    if (item.hasClass("event_item") || el.hasClass("event_item")) {
        if( el.hasClass("event_item") )
            item = el;
        // Item is the div that is required.
        
        $(".main_event_item").addClass("event_item"); // tell main_event it has data to show
        $(".main_event_item > div > div").hide(500);
        $(".main_event_item > div > div.title").show(500); // Show the title for the boxes.
        $(".main_event_item.event_item > div").show(500).removeClass( 'expand' ); // Tell the section that it is small.
        
        // Populate with events
        category_name = el.attr("id").substring(11);
        populate_event_group(category_name, $(".main_event_item"));

        // make other events smaller
        $(".event_items_div .event_item").removeClass("span3");
        $(".event_items_div .event_item").addClass("span1");
        $(".event_items_div .buffer").hide();
        $(".event_items_div .event_back").show();
        
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
    $(".event_items_div .event_item").removeClass("span1");
    $(".event_items_div .event_item").addClass("span3");
    $(".event_items_div .buffer").show();
    $(".event_items_div .event_back").hide();
}


/* ---------- Shows the page which has list of pages for an event -------- */
function show_event(me) {
    var $el = $( '.main_event_item.event_item' ),
        $sections = $el.children( 'div' ),
        $section = $(me).parent();

    $(".main_event_item.event_item").removeClass("rows_0") // gen
    $(".main_event_item.event_item").removeClass("rows_1")
    $(".main_event_item.event_item").removeClass("rows_2")
    $(".main_event_item.event_item").removeClass("rows_3")
    $(".main_event_item.event_item").addClass("rows_2")

    
    // expand the clicked section and hide the others
    $section.children(".event_content").addClass("loading")
    $sections.hide();
    $section.show();
    $sections.removeClass( 'expand' );
    $section.addClass( 'expand' );
    $section.addClass( 'expand' );
    $section.children("div").hide();
    $($section.children("div").get(1)).show();
    
    //change background of the clicked section
//    bg_new = $section.css("background").replace(/\d\D[\d]+\)/, "0.1)");
//    $section.css({"background":"rgba(57, 76, 73, 0.10)"});
};

// A function to bring a person from the event main page to the event group page
function hide_event () {
    var $el = $( '.main_event_item.event_item' ),
        $sections = $el.children( 'div' );

    $(".main_event_item.event_item").removeClass("rows_0") // gen
    $(".main_event_item.event_item").removeClass("rows_1")
    $(".main_event_item.event_item").removeClass("rows_2")
    $(".main_event_item.event_item").removeClass("rows_3")
    $(".main_event_item.event_item").addClass("rows_" + ( 1 + Math.floor($sections.length/4) ))

    $sections.show();
    $sections.removeClass( 'expand' );
    $sections.children("div").hide();
    $sections.each(function(){
        $($(this).children("div").get(0)).show();
    });
}

/* -------------------- EVENT PAGE ----------------- */

// A function to bring a person from the event main page to a specific page
function show_event_page(me) {
    var elem_number = $(me).index(),
        $section = $($( '.main_event_item.event_item > div.expand > div' ).get(1));
//    $('.sidr li')
    $(me).addClass("active");
    if ( elem_number != -1 ) {
        $section.children("div").slice(2).hide(500);
        $($section.children("div").slice(2).get(elem_number)).show(500); // +1 as title will also be there
        $(me).parent().children("li").removeClass("active");
        $(me).addClass("active");
    }
}

function got_event(json_event) { // post processing after josn is got
    Dajax.process(json_event)
    setTimeout( function() {
        var lst = $( '.main_event_item.event_item > div.expand p' );
        for ( var i = 0; i < lst.length; i++ ) {
            lst[i].removeAttribute("style");
        }
        lst = $( '.main_event_item.event_item > div.expand div' )
        for ( var i = 0; i < lst.length; i++ ) {
            lst[i].removeAttribute("style");
        }
    }, 1000);
}

// A function to bring a person from the event-page to the event main page
function hide_event_page() {
    var $section = $( '.main_event_item.event_item > div.expand' );
    
    $section.children("div").hide();
    $($section.children("div").get(1)).show(); // +1 as title will also be there
    
}
