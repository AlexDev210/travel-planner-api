# Travel Planner API

A backend REST API for planning trips and saving places validated against the Art Institute of Chicago API. Built with FastAPI and SQLite.

## How to run

### Option 1: Docker
docker build -t travel-planner-api .
docker run -d -p 8000:8000 --name travel_api travel-planner-api

### Option 2: Local Environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload

## API Documentation (Postman / Swagger)

FastAPI automatically generates an OpenAPI schema. Once the app is running, you can test all endpoints directly in your browser via the interactive Swagger UI:
http://127.0.0.1:8000/docs

## Environment Variables

No .env file is required for this assessment. The app is configured to use a local SQLite database, which will be generated automatically in the root folder upon the first run.

## Example Request

POST /projects/

{
  "name": "Weekend in Chicago",
  "description": "Art museum tour",
  "start_date": "2024-05-15",
  "places": [
    {
      "external_id": 129884,
      "notes": "Must see the Starry Night!",
      "visited": false
    }
  ]
}