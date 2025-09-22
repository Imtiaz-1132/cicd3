# File: D:\SEL\CICD3\test\test_code.py

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add src folder to sys.path so Python can find ptest.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ptest import api  # Import the FastAPI app

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}


def test_add_book():
    book = {
        "id": 1,
        "name": "Book One",
        "description": "First test book",
        "isAvailable": True
    }
    response = client.post("/book", json=book)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Book One"


def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1


def test_update_book():
    updated_book = {
        "id": 1,
        "name": "Updated Book",
        "description": "Updated description",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_book)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Book"
    assert data["isAvailable"] is False


def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Verify book is deleted
    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == []
