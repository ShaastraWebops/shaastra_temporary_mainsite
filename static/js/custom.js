
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
});
