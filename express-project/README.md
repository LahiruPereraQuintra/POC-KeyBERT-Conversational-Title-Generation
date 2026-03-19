# express-project

Express.js proxy that forwards title generation requests to the Python FastAPI service.

## Run

```bash
npm install
```

```bash
node src/index.js
```

## Endpoint

POST `/api/title/generate`

Request:
```json
{ "query": "string" }
```

