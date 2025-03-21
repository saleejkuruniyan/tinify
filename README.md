# URL Shortener API

A simple Django REST Framework-based URL shortener API that allows users to shorten long URLs and redirect using short codes.

## Features
- Shorten long URLs into short codes
- Redirect to the original URL using the short code
- Prevents duplicate short codes for the same URL
- Validates the provided long URLs
- Rate limiting to prevent abuse (10 requests per minute per IP)

## Endpoints

### 1. Shorten URL
- **URL:** `/shorten/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "long_url": "https://www.example.com"
  }
  ```
- **Response:**
  ```json
  {
    "short_url": "https://your-domain.com/abc123"
  }
  ```
- **Status Codes:**
  - `201 Created`: When a new short URL is created
  - `200 OK`: When the URL already exists
  - `400 Bad Request`: If the URL is invalid or missing
  - `429 Too Many Requests`: If the rate limit is exceeded

### 2. Redirect to Long URL
- **URL:** `/<short_code>`
- **Method:** `GET`
- **Response:** Redirects to the original long URL
- **Status Codes:**
  - `302 Found`: Successful redirection
  - `404 Not Found`: If the short code does not exist

### 3. Home Page
- **URL:** `/`
- **Method:** `GET`
- **Response:** Renders the home page for the URL shortener application.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saleejkuruniyan/tinify.git
   cd tinify
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## Configuration

Ensure you have the following in your `settings.py`:
```python
DOMAIN = "https://your-domain.com"
```

## Running Tests

```bash
python manage.py test
```

## Example Usage

- **Shorten URL:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"long_url": "https://www.example.com"}' \
       https://your-domain.com/shorten/
  ```

- **Redirect:**
  Visit `https://your-domain.com/abc123` in your browser.

## Rate Limiting

- Each IP is limited to **10 requests per minute** for URL shortening.
- If exceeded, the API returns:
  ```json
  {
    "detail": "Request was throttled. Expected available in 60 seconds."
  }
  ```

## Frontend Error Handling

The HTML interface now handles errors, including rate limits. Users will see messages like:
- "Please enter a URL."
- "Invalid URL."
- "Request was throttled. Expected available in 60 seconds."
- "An unexpected error occurred."

Make sure to refresh the browser to load the latest changes.
