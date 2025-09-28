import * as csvParser from '../../node_modules/csv-parser/index';
import * as fs from 'fs';
import { Connection } from "../classes/connection";
import { resolve } from 'path';


export function parseCSV(filePath: string): Promise<Connection[]> {
  return new Promise((resolve, reject) => {
    const results: Connection[] = [];
    
    fs.createReadStream(filePath)
      .pipe(csvParser())
      .on('data', (row) => {
        results.push(new Connection(
        row['Route ID'],
        row['Departure City'],
        row['Arrival City'],
        row['Departure Time'],
        row['Arrival Time'],
        parseFloat(row['First Class ticket rate (in euro)']),
        parseFloat(row['Second Class ticket rate (in euro)']),
        row['Train Type'],
        row['Days of Operation']
        ));
      })
      .on('end', () => {
        resolve(results);
      })
      .on('error', (err) => {
        reject(err);
      });
  });
}

