# graph class
from ..csv_read import read_csv
from .station import Station

class StationNetworkManager:
    def __init__(self):
        self.stations = {}  # key: city name, value: station object
        

    def load_connections(self,file_path: str):
        global connections
        # parse CSV here and populate `connections` list
        
        try:
            print(f"Loading connections from {file_path}...")
            connections = read_csv(file_path)
            print(f"Loaded {len(connections)} connections.")
            
            return connections
        except Exception as e:
            print(f"Error loading connections: {e}")
            return []
            
    def load_network(self,file_path: str):
        self.connections = self.load_connections(file_path)
        
        for connection in self.connections:
            if connection.departure_city not in self.stations:
                self.stations[connection.departure_city] = Station(connection.departure_city)
            
            station = self.stations[connection.departure_city]
            station.add_connection(connection)
            
    
            
