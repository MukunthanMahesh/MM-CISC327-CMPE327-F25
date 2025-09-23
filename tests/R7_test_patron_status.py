import pytest
import random
from datetime import datetime, timedelta
from database import init_database, get_db_connection, insert_book, insert_borrow_record
from library_service import get_patron_status_report

# assume get_patron_status_report(patron_id) has been implemented

# verify report returns error for invalid patron ID
def test_patron_status_invalid_id(tmp_path, monkeypatch):
    test_db = tmp_path / "test_library.db"
    monkeypatch.setattr("database.DATABASE", str(test_db))
    init_database()

    result = get_patron_status_report("12")
    assert "error" in result
    assert "invalid patron id" in result["error"].lower()

# verify report shows no loans and no fees if patron has borrowed nothing
def test_patron_status_no_loans(tmp_path, monkeypatch):
    test_db = tmp_path / "test_library.db"
    monkeypatch.setattr("database.DATABASE", str(test_db))
    init_database()

    result = get_patron_status_report("123456")
    assert result["patron_id"] == "123456"
    assert result["borrowed_count"] == 0
    assert result["total_late_fees"] == 0.0
    assert result["current_loans"] == []
    assert isinstance(result["history"], list)

# verify report includes a currently borrowed book
def test_patron_status_with_current_loan(tmp_path, monkeypatch):
    test_db = tmp_path / "test_library.db"
    monkeypatch.setattr("database.DATABASE", str(test_db))
    init_database()

    isbn = str(random.randint(1000000000000, 9999999999999))
    conn = get_db_connection()
    insert_book("Test Book", "Author A", isbn, 1, 0)
    borrow_date = datetime.now() - timedelta(days=2)
    due_date = borrow_date + timedelta(days=14)
    insert_borrow_record("123456", 1, borrow_date, due_date)
    conn.close()

    result = get_patron_status_report("123456")
    assert result["borrowed_count"] == 1
    assert result["total_late_fees"] == 0.0
    assert len(result["current_loans"]) == 1
    assert result["current_loans"][0]["title"] == "Test Book"

# verify report calculates late fees for patron correctly
def test_patron_status_with_late_fee(tmp_path, monkeypatch):
    test_db = tmp_path / "test_library.db"
    monkeypatch.setattr("database.DATABASE", str(test_db))
    init_database()

    isbn = str(random.randint(1000000000000, 9999999999999))
    conn = get_db_connection()
    insert_book("Late Book", "Author B", isbn, 1, 0)
    borrow_date = datetime.now() - timedelta(days=20)
    due_date = borrow_date + timedelta(days=14) 
    insert_borrow_record("123456", 1, borrow_date, due_date)
    conn.close()

    result = get_patron_status_report("123456")
    assert result["borrowed_count"] == 1
    assert result["total_late_fees"] > 0.0
    assert len(result["current_loans"]) == 1
    assert result["current_loans"][0]["title"] == "Late Book"

# verify borrowing history is recorded
def test_patron_status_history_includes_records(tmp_path, monkeypatch):
    test_db = tmp_path / "test_library.db"
    monkeypatch.setattr("database.DATABASE", str(test_db))
    init_database()

    isbn1 = str(random.randint(1000000000000, 9999999999999))
    isbn2 = str(random.randint(1000000000000, 9999999999999))
    conn = get_db_connection()
    insert_book("History Book 1", "Author C", isbn1, 1, 0)
    insert_book("History Book 2", "Author D", isbn2, 1, 0)
    borrow_date = datetime.now() - timedelta(days=10)
    due_date = borrow_date + timedelta(days=14)
    insert_borrow_record("123456", 1, borrow_date, due_date)
    insert_borrow_record("123456", 2, borrow_date, due_date)
    conn.close()

    result = get_patron_status_report("123456")
    assert isinstance(result["history"], list)
    assert len(result["history"]) >= 2
    titles = [h["title"] for h in result["history"]]
    assert "History Book 1" in titles
    assert "History Book 2" in titles
