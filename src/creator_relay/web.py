"""Loopback-only demo UI for Creator Relay."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from .relay import CreatorBrief, MindRelay, channels


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        MIND_EMAIL=os.getenv("CREATOR_RELAY_MIND_EMAIL", ""),
        MIND_ID=os.getenv("CREATOR_RELAY_MIND_ID", ""),
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/brief")
    def make_brief():
        payload = request.get_json(silent=True) or {}
        try:
            brief = CreatorBrief(
                source=str(payload.get("source", "")),
                audience=str(payload.get("audience", "")),
                channels=channels(payload.get("channels", [])),
                goal=str(payload.get("goal", "")),
            )
            relay = MindRelay(app.config["MIND_EMAIL"], app.config["MIND_ID"])
            preview = relay.local_preview(brief)
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(
            {
                "preview": preview,
                "mind_configured": relay.configured,
                "live_delivery": False,
                "notice": (
                    "No Mind message was sent. Configure both Mind ID and Mind "
                    "Email, then use an owner-approved delivery transport."
                ),
            }
        )

    return app
