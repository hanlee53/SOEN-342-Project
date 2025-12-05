# OCL Expressions for RailConnect Reservation System

**Course:** SOEN-342  
**Project:** RailConnect  
**Team Members:**  
- Han Lee (40265531)  
- Steven Ly (40215469)  
- Nguyen Le (40272922)

---

## 1. OCL Expression for the Method that Creates a Reservation

The `book_trip` method is responsible for creating a new reservation (Trip) in the system. This method takes a selected trip option, traveller details, and a day of week, then creates the appropriate Trip and Ticket objects.

```ocl
context BookingService::book_trip(selected_ticket: TripOption, traveller_details: List[Dict], day_of_week: int): Trip

pre:
**-- the selected ticket option must be defined and contain at least one connection**
selected_ticket.isDefined() and selected_ticket.connections->notEmpty()
**-- there must be at least one traveller to book**
traveller_details->notEmpty()
**-- all traveller details must have required fields: id, first_name, last_name, and age**
traveller_details->forAll(td | 
    td.id.isDefined() and 
    td.first_name.isDefined() and 
    td.last_name.isDefined() and 
    td.age.isDefined())
**-- age must be non-negative for all travellers**
traveller_details->forAll(td | td.age >= 0)
**-- day of week must be a valid value (0-6, representing Monday-Sunday)**
day_of_week >= 0 and day_of_week <= 6
**-- no duplicate client IDs within the booking request**
**-- i.e. if same client ID appears, then it must be a different traveller detail entry**
traveller_details->forAll(t1, t2 | t1 <> t2 implies t1.id <> t2.id)
**-- no client can have overlapping route reservations on the same day**
**-- i.e. for each client in traveller_details, check that they don't already have a ticket**
**-- for any of the routes in selected_ticket on the specified day_of_week**
traveller_details->forAll(td |
    Ticket.allInstances()->select(existing |
        existing.client.client_id = td.id and
        existing.day_of_week = day_of_week and
        selected_ticket.connections->exists(c | 
            existing.route_ids.split(",")->includes(c.route_id)
        )
    )->isEmpty()
)

post:
**-- a reservation (Trip) has been created and returned**
result.isDefined() and result.trip_id > 0 and result.created_at.isDefined()
**-- the number of tickets created equals the number of travellers**
result.tickets->size() = traveller_details->size()
**-- all tickets belong to the created trip**
result.tickets->forAll(t | t.trip = result)
**-- all tickets have the same departure and arrival cities as the selected ticket**
result.tickets->forAll(t | 
    t.departure_city = selected_ticket.departure_city.value and
    t.arrival_city = selected_ticket.arrival_city.value)
**-- all tickets have the same departure and arrival times as the selected ticket**
result.tickets->forAll(t | 
    t.departure_time = selected_ticket.departure_time and
    t.arrival_time = selected_ticket.arrival_time)
**-- all tickets have the same day of week as specified**
result.tickets->forAll(t | t.day_of_week = day_of_week)
**-- all tickets have the same route IDs as the selected ticket**
**-- i.e. each ticket's route_ids contains all route IDs from selected_ticket.connections**
result.tickets->forAll(t |
    selected_ticket.connections->forAll(c |
        t.route_ids.split(",")->includes(c.route_id)
    )
)
**-- each ticket corresponds to one of the provided traveller details**
result.tickets->forAll(t | 
    traveller_details->exists(td | 
        td.id = t.client.client_id and
        td.first_name = t.client.first_name and
        td.last_name = t.client.last_name and
        td.age = t.client.age))
**-- no duplicate clients within the created trip**
result.tickets->forAll(t1, t2 | 
    t1 <> t2 implies t1.client <> t2.client)
**-- the number of trips in the system has been increased by 1**
Trip.allInstances()->size() = Trip.allInstances()@pre->size() + 1
**-- the number of tickets in the system has been increased by the number of travellers**
Ticket.allInstances()->size() = Ticket.allInstances()@pre->size() + traveller_details->size()
```

---

## 2. OCL Expression for the Class that Represents a Reservation

The `Ticket` class represents a reservation in the system. A ticket contains all the reservation details for a specific passenger (client) on a journey, including departure and arrival information, route details, pricing, and day of travel.

```ocl
context Ticket

inv: self.trip.isDefined()
    **-- Every ticket must belong to a trip**

inv: self.client.isDefined()
    **-- Every ticket must have an associated client (passenger)**

inv: self.departure_city.isDefined() and self.departure_city->notEmpty()
    **-- Departure city must be defined and non-empty**

inv: self.arrival_city.isDefined() and self.arrival_city->notEmpty()
    **-- Arrival city must be defined and non-empty**

inv: self.departure_city <> self.arrival_city
    **-- Departure and arrival cities must be different**

inv: self.departure_time.isDefined()
    **-- Departure time must be defined**

inv: self.arrival_time.isDefined()
    **-- Arrival time must be defined**

inv: self.departure_time < self.arrival_time
    **-- Departure time must be before arrival time**

inv: self.price >= 0
    **-- Price must be non-negative**

inv: self.route_ids.isDefined() and self.route_ids->notEmpty()
    **-- Route identifiers must be defined and non-empty**

inv: self.route_ids.split(",")->forAll(rid | rid->notEmpty())
    **-- All route identifiers in the comma-separated list must be non-empty**

inv: self.day_of_week >= 0 and self.day_of_week <= 6
    **-- Day of week must be a valid value (0-6, representing Monday-Sunday)**
```
