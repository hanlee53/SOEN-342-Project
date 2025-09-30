import csv
from .classes.Connection import Connection

def read_csv(rail_network_csv_path: str):
    with open(rail_network_csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        list_connections = []
        for row in csv_reader:
            
            connection = Connection(
                route_id=row['Route ID'],
                departure_city=row['Departure City'],
                arrival_city=row['Arrival City'],
                departure_time=row['Departure Time'],
                arrival_time=row['Arrival Time'],
                days_of_operation=row['Days of Operation'],
                train_type=row['Train Type'],
                first_class_price=row['First Class ticket rate (in euro)'],
                second_class_price=row['Second Class ticket rate (in euro)']
            )
            
            list_connections.append(connection)
        return list_connections

