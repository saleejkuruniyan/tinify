# URL Shortener Service

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install django
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Usage
- POST to `/shorten` with `{ "long_url": "http://example.com" }` to get a short URL.
- Access the short URL to be redirected to the original URL.

## Testing
Run tests with:
```bash
python manage.py test
```
"""