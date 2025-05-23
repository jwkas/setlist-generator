# Setlist Generator

A web application for musicians and band managers to generate optimized setlists based on song parameters.

## Features

- Manage your band's song repertoire
  - Add songs manually or via CSV upload
  - Track song parameters like tempo, key, intensity, and vocalist
  - Mark favorite songs as "hits" to include in every setlist

- Generate setlists that follow these rules:
  - Never have more than two minor songs in a row
  - Never have more than two fast songs in a row
  - Never have more than two songs from the same vocalist in a row
  - Respect total setlist duration
  - Always include "hit" songs
  - Never have more than two original songs in a row
  - Never have two slow songs in a row
  - The second half of the set should have roughly the same number of original songs as the first half
  - The second half of the set should have roughly the same number of minor key songs as the first half
  - The second half of the set should have roughly the same number of slow and fast songs as the first half

## Technology Stack

- **Frontend**: Angular
- **Backend**: Python with Flask
- **Database**: SQLite

## Project Structure

```
setlist-generator/
├── backend/            # Flask API
│   ├── app.py          # Main application file
│   ├── models.py       # Database models
│   ├── routes.py       # API endpoints
│   └── requirements.txt # Python dependencies
│
├── frontend/           # Angular application
│   ├── src/            # Source files
│   └── ...             # Angular project files
│
└── README.md           # This file
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the Flask application: `python app.py`

### Frontend Setup

1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Run the Angular development server: `ng serve`
4. Open your browser to `http://localhost:4200`