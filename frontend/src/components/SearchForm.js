import React, { useState, useEffect } from 'react';

function SearchForm() {
  const [fromCity, setFromCity] = useState('');
  const [toCity, setToCity] = useState('');
  const [departureDate, setDepartureDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [passengers, setPassengers] = useState('1');
  const [departureCities, setDepartureCities] = useState([]);
  const [arrivalCities, setArrivalCities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [csvLoaded, setCsvLoaded] = useState(false);

  const handleSwap = () => {
    const temp = fromCity;
    setFromCity(toCity);
    setToCity(temp);
  };

  const handleFindConnections = () => {
    console.log('Finding connections...', { fromCity, toCity, departureDate, returnDate, passengers });
  };

  // Function to parse CSV data and extract cities
  const parseCSVAndExtractCities = (csvText) => {
    const lines = csvText.split('\n');
    const headers = lines[0].split(',');
    const data = [];

    // Find the indices of departure and arrival city columns
    const departureCityIndex = headers.findIndex(header => 
      header.trim().toLowerCase().includes('departure') && 
      header.trim().toLowerCase().includes('city')
    );
    const arrivalCityIndex = headers.findIndex(header => 
      header.trim().toLowerCase().includes('arrival') && 
      header.trim().toLowerCase().includes('city')
    );

    if (departureCityIndex === -1 || arrivalCityIndex === -1) {
      console.error('Could not find departure or arrival city columns');
      return;
    }

    // Parse CSV data
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        const values = lines[i].split(',');
        if (values[departureCityIndex] && values[arrivalCityIndex]) {
          data.push({
            departureCity: values[departureCityIndex].trim(),
            arrivalCity: values[arrivalCityIndex].trim()
          });
        }
      }
    }

    // Extract unique cities
    const uniqueDepartureCities = [...new Set(data.map(route => route.departureCity))].sort();
    const uniqueArrivalCities = [...new Set(data.map(route => route.arrivalCity))].sort();
    
    setDepartureCities(uniqueDepartureCities);
    setArrivalCities(uniqueArrivalCities);
    setCsvLoaded(true);
  };

  // Listen for CSV data from parent component
  useEffect(() => {
    const handleCSVData = (event) => {
      if (event.detail && event.detail.csvData) {
        parseCSVAndExtractCities(event.detail.csvData);
      }
    };

    window.addEventListener('csvDataLoaded', handleCSVData);
    return () => window.removeEventListener('csvDataLoaded', handleCSVData);
  }, []);

  return (
    <div className="search-card">
      <div className="search-form">
        {/* From/To Row */}
        <div className="search-row">
          <div className="search-field">
            <label className="field-label">From</label>
            <select
              value={fromCity}
              onChange={(e) => setFromCity(e.target.value)}
              className="city-select"
              disabled={!csvLoaded}
            >
              <option value="">
                {csvLoaded ? "Select departure city" : "Load CSV data first"}
              </option>
              {departureCities.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>
          
          <button className="swap-btn" onClick={handleSwap}>
            ⇄
          </button>
          
          <div className="search-field">
            <label className="field-label">To</label>
            <select
              value={toCity}
              onChange={(e) => setToCity(e.target.value)}
              className="city-select"
              disabled={!csvLoaded}
            >
              <option value="">
                {csvLoaded ? "Select destination city" : "Load CSV data first"}
              </option>
              {arrivalCities.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Date/Passengers Row */}
        <div className="search-row">
          <div className="search-field">
            <label className="field-label">Departure</label>
            <input
              type="date"
              value={departureDate}
              onChange={(e) => setDepartureDate(e.target.value)}
              className="date-input"
            />
          </div>
          
          <div className="search-field">
            <label className="field-label">Return</label>
            <input
              type="date"
              value={returnDate}
              onChange={(e) => setReturnDate(e.target.value)}
              className="date-input"
            />
          </div>
          
          <div className="search-field">
            <label className="field-label">Passengers</label>
            <select
              value={passengers}
              onChange={(e) => setPassengers(e.target.value)}
              className="passenger-select"
            >
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5+">5+</option>
            </select>
          </div>
        </div>

        {/* Find Connections Button */}
        <button className="find-btn" onClick={handleFindConnections}>
          🔍 Find Connections
        </button>
      </div>
    </div>
  );
}

export default SearchForm;
