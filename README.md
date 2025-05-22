# Setlist Generator

A web application for musicians and band managers to generate optimized setlists based on song parameters.

## Features

- Manage your band's song repertoire
  - Add songs manually or via CSV upload
  - Track song parameters like tempo, key, intensity, and vocalist
  - Mark favorite songs as "hits" to include in every setlist

- Generate balanced setlists that:
  - Evenly distribute major/minor keys
  - Evenly distribute tempos (slow, medium, fast)
  - Evenly distribute cover/original songs
  - Evenly distribute lead vocalist duties
  - Respect total setlist duration
  - Always include "hit" songs

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