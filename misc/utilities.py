#This will store all our utility functions

from django.core.exceptions import ValidationError
from django.utils import simplejson

# _____________--- DAJAX Alert Message ---______________#
def show_alert(dajax_, type_, msg_):
    """
        Give an alert in the bootstrap styled alert which is in base.html
    """
    dajax_.remove_css_class("#id_alert", "alert-success")
    dajax_.remove_css_class("#id_alert", "alert-warning")
    dajax_.remove_css_class("#id_alert", "alert-error")
    dajax_.remove_css_class("#id_alert", "alert-info")
    dajax_.remove_css_class("#id_alert", "hide")
    
    dajax_.add_css_class("#id_alert", "alert-" + type_.lower())
    dajax_.assign("#id_alert", "innerHTML", "<button type='button' class='close' onclick='javascript:js_alert_hide();'>&times;</button><strong>" + type_.upper() + "!</strong> " + msg_);
