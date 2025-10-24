from django.apps import AppConfig
from transit.services.station_network_manager import StationNetworkManager
import json

CSV_FILE_PATH = "./transit/data/eu_rail_network.csv"

class BackendDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_django'
    
    def ready(self):
        station_network_manager = StationNetworkManager(CSV_FILE_PATH)
        
