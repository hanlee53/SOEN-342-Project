# RailConnect Frontend

A modern React application for finding European rail connections with an intuitive search interface and CSV data support.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 16.0 or higher)
- **npm** (comes with Node.js)
- **Git** (for version control)

### Check Your Installation

```bash
node --version
npm --version
git --version
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SOEN-342-Project/frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required dependencies including:
- React 18.2.0
- React DOM 18.2.0
- React Scripts 5.0.1
- Web Vitals 2.1.4

### 3. Start the Development Server

```bash
npm start
```

The application will open in your browser at `http://localhost:3000`.

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML template
├── src/
│   ├── components/         # React components
│   │   ├── Header.js       # Header with logo and theme toggle
│   │   ├── Hero.js         # Main title and subtitle
│   │   ├── SearchForm.js   # Search form with city dropdowns
│   │   └── ActionButtons.js # CSV upload and sample data buttons
│   ├── App.js              # Main application component
│   ├── App.css             # Application styles with theme support
│   ├── index.js            # Application entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## Usage

### 1. Load Rail Data

- Click **"Load Rail Data"** to upload a CSV file
- The CSV should contain columns: `Departure City`, `Arrival City`, etc.
- Once loaded, city dropdowns will be populated with data from your CSV

### 2. Search for Connections

- Select departure and destination cities from the dropdowns
- Choose departure and return dates
- Select number of passengers
- Click **"Find Connections"** to search

### 3. Theme Toggle

- Click the moon/sun button in the header to switch between dark and light modes
- All components will smoothly transition between themes

## Available Scripts

In the project directory, you can run:

### `npm start`
Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm test`
Launches the test runner in interactive watch mode.

### `npm run build`
Builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

### `npm run eject`
**Note: this is a one-way operation. Once you `eject`, you can't go back!**

## CSV Data Format

The application expects CSV files with the following structure:

```csv
Route ID,Departure City,Arrival City,Departure Time,Arrival Time,Train Type,Days of Operation,First Class ticket rate (in euro),Second Class ticket rate (in euro)
R00003,A Coruña,Santander,12:05,14:17,RJX,Fri-Sun,115,70
R00004,A Coruña,Santander,12:50,15:54,ICE,Daily,97,69
```

## Development

### Adding New Components

1. Create your component in `src/components/`
2. Import and use it in `App.js`
3. Add any component-specific styles to `App.css`

### Styling Guidelines

- Use CSS classes with theme support
- Add `body.dark-mode` and `body.light-mode` selectors for theme variants
- Use smooth transitions: `transition: all 0.3s ease`

### State Management

- Each component manages its own state using React hooks
- Use `useState` for local state
- Use `useEffect` for side effects
- Custom events for component communication

## Troubleshooting

### Common Issues

**Port 3000 is already in use:**
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9
# Or use a different port
PORT=3001 npm start
```

**Dependencies not installing:**
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json
# Reinstall
npm install
```

**CSV not loading:**
- Ensure your CSV file has the correct column headers
- Check browser console for error messages
- Verify the file is a valid CSV format

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

