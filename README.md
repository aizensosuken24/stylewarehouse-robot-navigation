# StyleWarehouse Robot Navigation

A warehouse robot simulation that plans pick routes with A* pathfinding and a nearest-neighbour TSP sequencer. The project now includes a deployable Python WSGI app for GitHub, Vercel, and Render.

## Repository

- GitHub: `https://github.com/aizensosuken24/stylewarehouse-robot-navigation`

## Local Run

```bash
python -m pip install -r requirements.txt
python main.py
```

Auto demo:

```bash
python main.py --auto
```

Optional pygame visualiser:

```bash
python main.py --auto --pygame
```

## Tests

```bash
python -m pytest -q
```

## API Endpoints

The deployable app lives in [app.py](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/app.py).

- `GET /`
- `GET /api/health`
- `GET /api/catalogue`
- `GET /api/catalogue?search=tee&limit=5`
- `GET /api/catalogue/SW001`
- `GET /api/demo-order`
- `POST /api/simulate-order`

Example request:

```bash
curl -X POST http://localhost:8000/api/simulate-order ^
  -H "Content-Type: application/json" ^
  -d "{\"order_id\":\"API-001\",\"items\":[{\"sku\":\"SW001\",\"quantity\":1}]}"
```

## Deployment

### Vercel

- Entry point: [api/index.py](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/api/index.py)
- Routing config: [vercel.json](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/vercel.json)
- All routes are forwarded to the Python WSGI app.

### Render

- Blueprint config: [render.yaml](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/render.yaml)
- Start command: `gunicorn app:app`

## Internationalisation

English fallback strings are built in, and Hindi and Telugu translations live in:

- [src/i18n/translations/hi.json](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/src/i18n/translations/hi.json)
- [src/i18n/translations/te.json](/c:/Users/ANIRUDH/OneDrive/Desktop/stylewarehouse-robot-navigation-final/src/i18n/translations/te.json)
