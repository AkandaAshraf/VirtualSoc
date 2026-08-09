import io
import time
import zipfile

import pytest

from webapp import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def wait_for(client, job_id, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        j = client.get(f"/api/jobs/{job_id}").get_json()
        if j["status"] in ("done", "error"):
            return j
        time.sleep(0.2)
    raise AssertionError("job did not finish in time")


def run_small_sim(client, **overrides):
    body = {"n_people": 40, "n_groups": 2, "time_steps": 2,
            "exploration_probability": 0.8, "connection_percentage": 5,
            "seed": 7, "attributes": {"preset": "default_social"}}
    body.update(overrides)
    r = client.post("/api/simulate", json=body)
    assert r.status_code == 202, r.get_json()
    job_id = r.get_json()["job_id"]
    status = wait_for(client, job_id)
    assert status["status"] == "done", status
    return job_id


def test_limits_endpoint(client):
    j = client.get("/api/limits").get_json()
    assert "n_people" in j["limits"] and "multihot" in j["feature_kinds"]


def test_simulate_end_to_end_with_preset(client):
    job_id = run_small_sim(client)
    res = client.get(f"/api/jobs/{job_id}/result").get_json()
    assert len(res["nodes"]) == 40
    assert len(res["snapshots"]) == 2
    assert res["snapshots"][1]["stats"]["edges"] >= res["snapshots"][0]["stats"]["edges"]
    assert set(n["label"] for n in res["nodes"]) == {0, 1}
    assert len(res["nodes"][0]["encoded"]) == len(res["encoded_feature_names"])
    assert "homophily" in res["snapshots"][0]["stats"]


def test_simulate_with_custom_attributes(client):
    job_id = run_small_sim(client, attributes={"specs": [
        {"name": "age", "kind": "numeric", "preset": "age"},
        {"name": "income", "kind": "numeric", "low": 0, "high": 90000},
        {"name": "gender", "kind": "binary", "p_one": 0.5},
        {"name": "city", "kind": "categorical", "n_categories": 6},
        {"name": "interests", "kind": "multihot", "n_items": 8},
    ]})
    res = client.get(f"/api/jobs/{job_id}/result").get_json()
    assert [a["name"] for a in res["schema"]] == [
        "age", "income", "gender", "city", "interests"]
    assert len(res["nodes"][0]["encoded"]) == 1 + 1 + 1 + 6 + 8


def test_download_zip_contents(client):
    job_id = run_small_sim(client)
    r = client.get(f"/api/jobs/{job_id}/download")
    assert r.status_code == 200
    z = zipfile.ZipFile(io.BytesIO(r.data))
    names = set(z.namelist())
    assert {"params.json", "schema.json", "labels.csv",
            "features_encoded.csv", "features_typed.json",
            "edges_t0.csv", "edges_t1.csv", "stats.json",
            "README.txt"} <= names
    labels = z.read("labels.csv").decode().strip().splitlines()
    assert labels[0] == "node_id,label" and len(labels) == 41


def test_validation_rejects_bad_requests(client):
    assert client.post("/api/simulate", json={"n_people": 5}).status_code == 400
    assert client.post("/api/simulate", json={"n_people": 999999}).status_code == 400
    r = client.post("/api/simulate", json={
        "n_people": 40, "attributes": {"specs": [{"name": "x", "kind": "nope"}]}})
    assert r.status_code == 400
    assert "kind" in r.get_json()["error"]


def test_unknown_job_returns_404(client):
    assert client.get("/api/jobs/doesnotexist").status_code == 404
