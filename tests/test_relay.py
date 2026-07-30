from creator_relay.relay import CreatorBrief, MindRelay
from creator_relay.memory import CreatorMemory
from creator_relay.web import create_app


BRIEF = CreatorBrief(
    source="A creator explains how a weekly behind-the-scenes series helped their audience understand the craft and ask better questions.",
    audience="independent video creators",
    channels=("YouTube", "X"),
    goal="invite discussion around the next episode",
)


def test_preview_is_not_a_claimed_mind_response():
    preview = MindRelay.local_preview(BRIEF)
    assert len(preview) == 2
    assert preview[0]["status"] == "local draft — needs Mind response"


def test_compose_requires_explicit_mind_identity():
    try:
        MindRelay(None).compose(BRIEF)
    except ValueError as exc:
        assert "explicitly configured" in str(exc)
    else:
        raise AssertionError("configuration should be required")


def test_composed_message_mentions_real_configured_identity():
    message = MindRelay("creator@example.test", "mind-demo-1").compose(BRIEF)
    assert message["To"] == "creator@example.test"
    assert "Mind ID: mind-demo-1" in message.get_content()


def test_web_api_is_explicitly_non_live():
    client = create_app().test_client()
    response = client.post(
        "/api/brief",
        json={
            "source": BRIEF.source,
            "audience": BRIEF.audience,
            "channels": list(BRIEF.channels),
            "goal": BRIEF.goal,
        },
    )
    assert response.status_code == 200
    assert response.json["live_delivery"] is False
    assert response.json["mind_configured"] is False


def test_memory_keeps_a_visible_brief_and_follow_up(tmp_path):
    memory = CreatorMemory(tmp_path / "creator-relay.sqlite3")
    remembered = memory.remember(BRIEF)
    timeline = memory.timeline()
    assert remembered["brief_id"] == 1
    assert timeline[0]["goal"] == BRIEF.goal
    assert timeline[0]["status"] == "queued"


def test_timeline_api_shows_persistence_without_claiming_delivery(tmp_path):
    app = create_app()
    app.config["MEMORY_DATABASE"] = str(tmp_path / "not_used_after_creation.sqlite3")
    client = app.test_client()
    created = client.post(
        "/api/brief",
        json={"source": BRIEF.source, "audience": BRIEF.audience,
              "channels": list(BRIEF.channels), "goal": BRIEF.goal},
    )
    history = client.get("/api/timeline")
    assert created.status_code == 200
    assert history.json["events"]
    assert history.json["live_delivery"] is False
