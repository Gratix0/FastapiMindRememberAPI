from tests.conftest import client


def test_add_one_folder():
    responce = client.post("/add_one_folder", json={
        "text_folder": "string",
        "number_of_topics": 0,
        "last_open_date_time": "2024-08-14T10:02:21.829Z"
    })
    assert responce.status_code == 200


def test_get_folders():
    responce = client.get("/folders")
    assert responce.status_code == 200


def test_add_theme():
    responce = client.post("/folders/1/add_theme", json={
        "name_theme": "string",
        "number_of_records": 0,
        "last_open_date_time": "2024-08-14T10:07:33.717Z"
    })
    assert responce.status_code == 200


def test_get_themes():
    responce = client.get("/folders/1/themes")
    assert responce.status_code == 200


def test_add_record():
    responce = client.post("/themes/1/add_record", json={
        "name_record": "string",
        "text_records": "string",
        "count_text": 0,
        "last_open_date_time": "2024-08-14T10:15:33.821Z"
    })
    assert responce.status_code == 200


def test_get_records():
    responce = client.get("/themes/1/records")
    assert responce.status_code == 200


def test_add_knowledge_queue():
    responce = client.post("/knowledge_queue", json={
        "content_knowledge_queue": "string",
        "completed_task_status": False,
        "number_of_cycles": 0,
        "create_date_time": "2024-08-14T10:17:26.894Z",
        "next_alert_card": "2024-08-14T10:17:26.894Z"
    })
    assert responce.status_code == 200


def test_get_knowledge_queue():
    responce = client.get("/knowledge_queue")
    assert responce.status_code == 200
