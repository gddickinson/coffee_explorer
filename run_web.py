"""Start the Coffee Collection Explorer web app on http://127.0.0.1:8104 (local only).

Run: python run_web.py   (needs: pip install -r requirements-web.txt)
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("web.app:app", host="127.0.0.1", port=8104)
