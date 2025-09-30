from enum import Enum

class DayOfWeek(Enum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

day_name_to_enum = {
    "Sun": DayOfWeek.Sunday,
    "Mon": DayOfWeek.Monday,
    "Tue": DayOfWeek.Tuesday,
    "Wed": DayOfWeek.Wednesday,
    "Thu": DayOfWeek.Thursday,
    "Fri": DayOfWeek.Friday,
    "Sat": DayOfWeek.Saturday,
}
