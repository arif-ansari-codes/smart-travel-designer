# Smart Travel Designer — AI-Powered Trip Planner

An AI travel planning app that generates personalized day-by-day itineraries with real weather forecasts, destination photos, cost estimates, and live exchange rates.

**Live App:** [ai-trip-frontend.vercel.app](https://ai-trip-frontend.vercel.app)

---

## Project Structure

```
ai-trip-planner/
├── backend/                  ← FastAPI (Python) — deployed on Render
│   ├── app/
│   │   ├── core/             ← Config and logging
│   │   ├── models/           ← Pydantic schemas
│   │   ├── routes/           ← API endpoints
│   │   └── services/         ← External API integrations
│   └── requirements.txt
├── frontend/                 ← Next.js (TypeScript) — deployed on Vercel
│   └── src/
│       ├── app/              ← Pages (home + trip planner)
│       ├── components/       ← UI components
│       ├── services/         ← API service layer
│       ├── types/            ← TypeScript interfaces
│       └── lib/              ← Zod validation schema
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS v4, shadcn/ui |
| Backend | FastAPI, Python, Uvicorn |
| AI | OpenAI GPT-4o |
| Weather | OpenWeatherMap API |
| Photos & Attractions | TripAdvisor Content API |
| Exchange Rates | ExchangeRate-API |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

---

## How It Works

1. User enters their name, home country, currency, destination country, city, and number of days
2. Backend fetches weather forecast, attractions, restaurants, and photos for the destination
3. All data is fed to GPT-4o to generate a personalized day-by-day itinerary
4. Response includes the trip summary, destination photos, weather forecast, exchange rate, and estimated daily costs

---

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root:

```
OPENWEATHER_KEY=your_key
OPENAI_API_KEY=your_key
TRIPADVISOR_KEY=your_key
EXCHANGE_RATE_API_KEY=your_key
ALLOWED_ORIGINS=http://localhost:3000
```

Run the server:

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

---

## Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Run the dev server:

```bash
npm run dev
```

App available at `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/trip-plan/` | Generate full trip plan |
| POST | `/weather/forecast` | Get weather forecast |
| POST | `/exchange-rate/` | Get exchange rate |
| POST | `/tripadvisor/data` | Get attractions, restaurants, photos |

---

## Deployment

- **Frontend** — connected to Vercel via the `ai-trip-frontend` GitHub repository. Auto-deploys on push to `main`.
- **Backend** — connected to Render via the `ai-trip-backend` GitHub repository. Auto-deploys on push to `main`. Set all environment variables (including `ALLOWED_ORIGINS`) in the Render dashboard.
