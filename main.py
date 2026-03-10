from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes import router

app = FastAPI()


@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    html = """
    <html>
    <head>
        <title>StudyMate API</title>
        <style>
            body { background-color: #1a1a1a; color: #f0f0f0; font-family: Arial, Helvetica, sans-serif; padding: 2rem; }
            h1 { color: #4fd1c5; }
            a { color: #90cdf4; text-decoration: none; }
            a:hover { text-decoration: underline; }
            pre { background-color: #2d2d2d; padding: 1rem; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>StudyMate – AI‑Powered Study Planner</h1>
        <p>Intelligent study‑plan generation, revision‑card creation and progress analytics.</p>
        <h2>Available Endpoints</h2>
        <ul>
            <li><strong>GET</strong> <code>/health</code> – health check</li>
            <li><strong>POST</strong> <code>/study-plans</code> – generate a 7‑day study plan</li>
            <li><strong>POST</strong> <code>/revision-cards</code> – generate revision flashcards</li>
        </ul>
        <h2>Documentation</h2>
        <ul>
            <li><a href="/docs" target="_blank">Swagger UI</a></li>
            <li><a href="/redoc" target="_blank">ReDoc</a></li>
        </ul>
        <h2>Tech Stack</h2>
        <pre>
FastAPI 0.115.0
PostgreSQL (psycopg)
DigitalOcean Serverless Inference (openai‑gpt‑oss‑120b)
        </pre>
    </body>
    </html>
    """
    return html
