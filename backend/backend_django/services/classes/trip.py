from datetime import timedelta

# this class represents a full trip consisting of one or more connections
# it calculates total travel duration, total price, number of connections, etc.
# it also provides a method to calculate total transfer time between connections

class Trip():
    def __init__(self, connections: list):
        self.connections = connections
        self.departure_city = connections[0].departure_city
        self.arrival_city = connections[-1].arrival_city
        self.total_travel_duration = sum([conn.duration for conn in connections], timedelta())
        self.total_first_class_price = sum([conn.first_class_price for conn in connections])  
        self.num_connections = len(connections) 
        self.total_second_class_price = sum([conn.second_class_price for conn in connections])
        self.isDirect = self.num_connections == 1
        self.departure_time = connections[0].departure_time
        self.arrival_time = connections[-1].arrival_time
        
    def calculate_transfer_time(self):
        total_transfer = timedelta()
        for i in range(len(self.connections) - 1):
            wait_time = self.connections[i+1].departure_time - self.connections[i].arrival_time
            if wait_time > timedelta():
                total_transfer += wait_time
        return total_transfer