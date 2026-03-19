# key-bert-project-python

FastAPI service that generates a chat title using KeyBERT (keyphrase extraction) + a zero-shot intent classifier.

## Run

```bash
pip install -r requirements.txt
```

Download the spaCy model required by `KeyphraseCountVectorizer`:

```bash
python -m spacy download en_core_web_sm
```

Then start the server:

```bash
uvicorn main:app --reload
```

## API

POST `/generate-title`

Request:
```json
{ "query": "string" }
```

Response:
```json
{ "title": "string", "keyphrase": "string", "intents": ["string"], "duration_ms": 0 }
```

