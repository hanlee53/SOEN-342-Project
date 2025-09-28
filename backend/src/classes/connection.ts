import { City, cityFromRaw } from "../enums/city-enum";
import { DayOfWeek, dayNameToEnum } from "../enums/day-of-week";
import { TrainType, trainTypeFromRaw } from "../enums/train-types";


export class Connection{
    private routeId: string;
    private cityFrom: City;
    private cityTo: City;
    private departureTime: Date;
    private arrivalTime: Date;
    private dayOffset: number;
    private daysOfOperation: Set<DayOfWeek>
    // in minutes
    private duration: number
    private trainType: TrainType;
    private firstClassPrice: number;
    private secondClassPrice: number;

    constructor(routeId: string, CityFrom: string, CityTo: string, DepartureTime: string, ArrivalTime: string, firstClassPrice: number, secondClassPrice: number, trainType: string, daysofOperation:string){
        this.routeId = routeId;
        this.cityFrom = this.parseCity(CityFrom);
        this.cityTo = this.parseCity(CityTo);
        this.departureTime = new Date(DepartureTime);
        this.parseAndSetArrivalTime(ArrivalTime);

        const durationMs = this.arrivalTime.getTime() - this.departureTime.getTime();
        const durationMinutes = durationMs / (1000 * 60);
        this.duration = durationMinutes

        this.trainType = trainTypeFromRaw[trainType]!;

        this.firstClassPrice = firstClassPrice;
        this.secondClassPrice = secondClassPrice;

        this.daysOfOperation = this.parseDaysOfOperation(daysofOperation);
    }

    private parseDaysOfOperation(daysStr: string): Set<DayOfWeek> {
        const daysSet = new Set<DayOfWeek>();

        if(daysStr.toLowerCase() === "daily") {
            Object.values(DayOfWeek).forEach(day => daysSet.add(day as DayOfWeek));
        } else if(daysStr.includes(",")) {
            const daysArray = daysStr.split(",").map(day => day.trim());
            for (const day of daysArray) {
                const dayEnum = (DayOfWeek as any)[day.toUpperCase()];
                if (dayEnum) {
                    daysSet.add(dayEnum);
                } else {
                    console.error(`Invalid day of operation: ${day}`);
                }
            }
        }else if(daysStr.includes("-")){
            const dayArr = daysStr.split("-").map(day => day.trim());
            
            if(dayArr.length !== 2){
                console.error(`Invalid range of days: ${daysStr}`);
                return daysSet;
            }

            const startDay = dayNameToEnum[dayArr[0]];
            const endDay =  dayNameToEnum[dayArr[1]];

            for(let i = startDay; ; i = (i + 1) % 7){
                daysSet.add(i);
                if(i === endDay) break;
            }
        }

        return daysSet
    }

    private parseAndSetArrivalTime(arrivalTimeStr: string): void {
        const parts = arrivalTimeStr.trim().split(" ");

        if (parts.length > 1) {
            const timePart = parts[0];
            const offsetPart = parts[1];
            const match = offsetPart.match(/\+(\d+)d/);

            if (!match || !match[1]) {
                console.error(`Invalid arrival time format: ${arrivalTimeStr}`);
                return;
            }

            const dayOffset = parseInt(match[1], 10);
            this.dayOffset = dayOffset;

            // Parse arrival time hours and minutes
            const [hours, minutes] = timePart.split(":").map(Number);

            // Create new Date based on departureTime with added days and set time
            const baseDate = new Date(this.departureTime.getTime()); // clone departure time
            baseDate.setDate(baseDate.getDate() + dayOffset);
            baseDate.setHours(hours, minutes, 0, 0);

            this.arrivalTime = baseDate;
        } else {
            // No offset, just parse time relative to departure date with dayOffset 0
            const [hours, minutes] = parts[0].split(":").map(Number);
            this.dayOffset = 0;

            const baseDate = new Date(this.departureTime.getTime());
            baseDate.setHours(hours, minutes, 0, 0);
            this.arrivalTime = baseDate;
        }
    }

    private parseCity(City: string): City {
        const cityValue = cityFromRaw[City.toLowerCase()]!;
        if (!cityValue) {
            console.error(`Invalid city value: ${City}`);
        }
        return cityValue;
    }
    
}