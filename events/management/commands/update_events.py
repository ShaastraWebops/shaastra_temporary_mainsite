# imports for registering a command
from django.core.management.base import BaseCommand, CommandError
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From shaasta_mainsite_2014
from mainsite_2014.settings import ERP_PROJECT_PATH
from events.models import Event_html_dump
from django.utils import timezone
# Python imports
import json
import os, datetime, glob
# events.ajax imports
from events.ajax import create_html_dump

class Command(BaseCommand):
    def handle(self, *args, **options):
        json_dir_path = os.path.abspath( os.path.join( ERP_PROJECT_PATH, 'media', 'json', 'events') )
        json_filepaths = glob.glob(json_dir_path + '/*.json')
        
        for event_json_filepath in json_filepaths:
            try:
                create_html_dump(len(json_dir_path)+1, event_json_filepath)
            except Exception as e:
                #raise CommandError("Problem updating json file: %s" %event_json_filepath)
                self.stderr.write("Problem updating json file: %s\n" %event_json_filepath)
                self.stderr.write("%s" % e)
                
                continue
                
        self.stdout.write("Updating events completed\n")
