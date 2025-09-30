import React, { useRef } from 'react';

function ActionButtons() {
  const fileInputRef = useRef(null);

  const handleLoadData = () => {
    // Trigger file input when button is clicked
    fileInputRef.current.click();
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
      console.log('CSV file selected:', file.name);
      const reader = new FileReader();
      reader.onload = (e) => {
        console.log('CSV content loaded');
        // Emit custom event with CSV data
        const csvDataEvent = new CustomEvent('csvDataLoaded', {
          detail: { csvData: e.target.result }
        });
        window.dispatchEvent(csvDataEvent);
      };
      reader.readAsText(file);
    } else {
      alert('Please select a valid CSV file');
    }
  };

  const handleSampleData = () => {
    console.log('Loading sample data...');
  };

  return (
    <div className="action-buttons">
      <div className="file-upload-container">
        <input
          type="file"
          accept=".csv"
          ref={fileInputRef}
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />
        <button className="load-data-btn" onClick={handleLoadData}>
          <span className="btn-icon">📊</span>
          Load Rail Data
        </button>
      </div>
      <button className="sample-data-btn" onClick={handleSampleData}>
        <span className="btn-icon">🚂</span>
        Sample Data
      </button>
    </div>
  );
}

export default ActionButtons;
