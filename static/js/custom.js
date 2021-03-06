
/* -- 03. SCROLL TO  -- */


$('ul.nav a, #down_button a').click(function(e) {
//    $('html, body').scrollTo(this.hash, this.hash);
    window.location.hash = this.hash + "_page";
    e.preventDefault();
    
});

/* -- 04. NAVBAR STICKY + SELECTED  -- */


$(function() {

    // Do our DOM lookups beforehand
    var nav_container = $(".navbar-wrapper");
    var nav = $(".navbar");

    var top_spacing = 0;
    var waypoint_offset = -80;

    nav_container.waypoint({
        handler: function(event, direction) {

            if (direction == 'down') {

                nav_container.css({'height': nav.outerHeight()});
                nav.stop().addClass("navbar-fixed-top").css("top", -nav.outerHeight()).animate({"top": top_spacing});
                $(".navbar .brand").html($(".navbar .brand_bw").html())

            } else {

                nav_container.css({'height': 'auto'});
                nav.stop().removeClass("navbar-fixed-top").css("top", nav.outerHeight() + waypoint_offset).animate({"top": ""});
                $(".navbar .brand").html($(".navbar .brand_color").html())
                
            }

        },
        offset: function() {
            return -nav.outerHeight() - waypoint_offset;
        }
    });

    var sections = $("body > section");
    var navigation_links = $("ul.nav a");

    sections.waypoint({
        handler: function(event, direction) {
            
            var active_section;
            active_section = $(this);
            if (direction === "up")
                active_section = active_section.prev();

            var active_link = $('ul.nav a[href="#' + active_section.attr("id") + '"]');
            navigation_links.removeClass("selected");
            active_link.addClass("selected");
            //window.location.hash=active_section.attr("id").replace(" ","_").lower()
            
        },
        offset: '25%'
    })


});

var black_h = $("#behind_banner_div > div").height();

$(window).scroll(function() {
    var ypos = window.pageYOffset;
    var h = $("body").height();
    //console.log(ypos + "   " + h);
    if(ypos < h) {
        var left_rad = 50 * (h-ypos) / h;
        var right_rad = 20 * (h-ypos) / h;
    //    console.log(h + " . " + ypos + " -- ", left_rad);
/*        $("#home > div#banner_div").css( {
            'border-bottom-left-radius' : left_rad + '% ' + right_rad + '%',
            'border-bottom-right-radius' : left_rad + '% ' + right_rad + '%',
            'height' : (h-ypos)*0.9 + 'px',
        } );*/        
        
        $('#banner_div').css( {
            'top' : ypos + 'px',
        } );
        $('#behind_banner_div').css( {
            'top' : ypos + 'px',
        } );
        
        //do stuff here
    }
    if(ypos < h*0.8) {
        $('.nav a[href="#home"]').addClass("active")
        $('.nav a').removeClass("selected")
        $('.nav a').removeClass("selected")
        hexa_init()
    } else {
        $('.nav a[href="#home"]').removeClass("active")
        clearInterval(hexa_pid)
        hexa_pid = -1;
    }
    if(ypos > $("#aboutus").offset().top + 8*$("#aboutus").height()/10 && ypos < $("#events").offset().top + 5*$("#events").height()/10) {
        if ( $("#modal_update_event").length  ) {
            $("#modal_update_event").removeClass("hide")
            $("#modal_update_event").css({
                "width" : ( $("body").width() - ( $("#modal_update_event").parent().children(".page_content").offset().left + $("#modal_update_event").parent().children(".page_content").width() ) - 50 ) +"px",
            })
        }
        if ( $("#modal_spons_event").length  ) {
            $("#modal_spons_event").removeClass("hide")
            $("#modal_spons_event").css({
                "width" : ( $("#modal_spons_event").parent().children(".sidr").offset().left  - 50 ) +"px",
            })
        }
    } else {
        if ( $("#modal_update_event").length ) {
            $("#modal_update_event").addClass("hide")
        }
        if ( $("#modal_spons_event").length ) {
            $("#modal_spons_event").addClass("hide")
        }
    }
});


// For the dashboard !
function do_accordion(elem_str, type) {
    elem_id = "#" + elem_str + "_head"
    elem_class_body = "." + elem_str + "_body"
    elem_head = $(elem_str)
    if ( type == "hide" || type == "show" )
        $(elem_class_body).collapse(type)
    else
        $(elem_class_body).collapse('toggle')
    elem_head.addClass("active_head")
    
    elem_head_i = $(elem_id + " a i")
    if( elem_head_i.hasClass("icon-chevron-down") ) {
        elem_head_i.removeClass("icon-chevron-down")
        elem_head_i.addClass("icon-chevron-up")
    } else {
        elem_head_i.removeClass("icon-chevron-up")
        elem_head_i.addClass("icon-chevron-down")
        
    }
} 
