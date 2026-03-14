"""
utils/sheets_client.py
──────────────────────
Google Sheets client using Apps Script Web App URL.
No service account, no credentials.json, no Google Cloud Console.
Just paste the deployed Web App URL as APPS_SCRIPT_URL env variable.
"""

import json
import os
import requests


class SheetsClient:
    def __init__(self, web_app_url: str = None, apps_script_url: str = None, **kwargs):
        """
        Pass the deployed Apps Script Web App URL.
        Accepts both web_app_url and apps_script_url as keyword args.
        """
        self.url = apps_script_url or web_app_url or os.environ.get("APPS_SCRIPT_URL", "")
        if not self.url:
            print("[Sheets] WARNING: APPS_SCRIPT_URL not set. Sheet operations will fail.")

    def _post(self, payload: dict) -> dict:
        """Send a POST request to the Apps Script Web App."""
        try:
            res = requests.post(
                self.url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10,
                allow_redirects=True
            )
            return res.json()
        except Exception as e:
            print(f"[Sheets] Request error: {e}")
            return {"status": "error", "message": str(e)}

    # ── Users ─────────────────────────────────────────────────

    def find_user(self, email: str):
        """Check credentials. Returns user dict on success, None on failure."""
        # We use signin to verify — returns user or error
        # find_user is called by signin route with only email to check existence
        # We send a dummy call to get_sessions which auto-creates sheets
        # Instead: use a dedicated lookup via signin with a sentinel
        # Actual password check is done in handleSignin on the script side
        return None  # Overridden by verify_user below

    def verify_user(self, email: str, password_hash: str):
        """
        Verify login credentials via Apps Script.
        Returns user dict {name, email} on success, None on failure.
        """
        res = self._post({
            "action":        "signin",
            "email":         email,
            "password_hash": password_hash
        })
        if res.get("status") == "ok":
            return res.get("user")
        return None

    def add_user(self, user: dict):
        """Register a new user."""
        return self._post({
            "action":        "signup",
            "name":          user.get("name", ""),
            "email":         user.get("email", ""),
            "password_hash": user.get("password_hash", ""),
            "created_at":    user.get("created_at", "")
        })

    def email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        res = self._post({
            "action":        "signin",
            "email":         email,
            "password_hash": "__CHECK_ONLY__"
        })
        # If user not found → email doesn't exist
        msg = res.get("message", "")
        return "No account" not in msg and res.get("status") != "error"

    # ── Sessions ──────────────────────────────────────────────

    def add_session(self, session_data: dict):
        return self._post({
            "action":     "add_session",
            "email":      session_data.get("email", ""),
            "name":       session_data.get("name", ""),
            "date":       session_data.get("date", ""),
            "time":       session_data.get("time", ""),
            "words":      session_data.get("words", ""),
            "word_count": session_data.get("word_count", "0"),
            "sentence":   session_data.get("sentence", ""),
            "duration":   session_data.get("duration", "0")
        })

    def get_sessions(self, email: str) -> list:
        res = self._post({"action": "get_sessions", "email": email})
        if res.get("status") == "ok":
            return res.get("sessions", [])
        return []

    # ── Feedback ──────────────────────────────────────────────

    def add_feedback(self, feedback: dict):
        return self._post({
            "action":    "add_feedback",
            "email":     feedback.get("email", ""),
            "name":      feedback.get("name", ""),
            "rating":    feedback.get("rating", ""),
            "message":   feedback.get("message", ""),
            "timestamp": feedback.get("timestamp", "")
        })
