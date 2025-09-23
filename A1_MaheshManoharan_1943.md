# CISC 327 - ASSIGNMENT 1
**Student Name :** Mukunthan Mahesh Manoharan  
**Student #    :** 20391943  
**Group        :** 3 (TA - Mir Nasreen)  

### Project Implementation Status
Below is the status of each required function as of submission time:

| Function                      | Implementation Status | What is Missing?                                                                                                               |
| ----------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `add_book_to_catalog`         | Complete              | N/A                                                                                                                            |
| `get_all_books`               | Complete              | N/A                                                                                                                            |
| `borrow_book_by_patron`       | Complete              | N/A                                                                                                                            |
| `return_book_by_patron`       | Partial               | Validate patron ID and book ID, verify the borrow, update available copes, record return date, calculate and display late fees |
| `calculate_late_fee_for_book` | Partial               | Calculate late fees based on specifications, return JSON response with fee amount and days overdue                             |
| `search_books_in_catalog`     | Partial               | Provide search functionality with terms and types, support partial/exact matching, return results in catalog display format    |
| `get_patron_status_report`    | Partial               | Display patron status for a particular patron with aggregated due dates, late fees, books borrowed and borrowing history       |


### Test Script Summary
All unit tests are stored in the (`tests/`) directory. Each functional requirement (R1–R7) has a dedicated test script named `RX_test_<feature>.py`. All database-related tests use `tmp_path` to create a temporary SQLite file and `monkeypatch` to override the DATABASE path.

- **R1_test_add_book.py**
  - `test_add_book_long_title()`: verify adding a book with overly long title fails
  - `test_add_book_valid_input()`: verify adding a book with valid input succeeds
  - `test_add_book_missing_title()`: verify adding a book with missing title fail
  - `test_add_book_invalid_isbn()`: verify adding a book with invalid ISBN fails
  - `test_add_book_invalid_copies()`: verify adding a book with negative copies fails  
  
- **R2_test_catalog_display.py**
  - `test_display_catalog_empty_database(tmp_path, monkeypatch)`: verify displaying catalog on empty database returns an empty list
  - `test_display_catalog_not_empty()`: verify displaying catalog returns non-empty list after adding sample data
  - `test_display_catalog_book_fields()`: verify each book in catalog has required fields
  - `test_display_catalog_ordered_by_title(tmp_path, monkeypatch):` verify catalog results are ordered alphabetically by title
  - `test_display_catalog_invalid_copies(tmp_path, monkeypatch)`: verify displaying catalog can handle invalid data without breaking  
  
- **R3_test_borrow_book.py**
  - `test_borrow_book_no_availability(tmp_path, monkeypatch)`: verify borriwng fails if book has zero available copies
  - `test_borrow_book_valid_input(tmp_path, monkeypatch)`: verify borrowing succeeds with valid patron and available book
  - `test_borrow_book_invalid_patron_id(tmp_path, monkeypatch)`: verify borrowing fails with invalid patron ID
  - `test_borrow_book_not_found(tmp_path, monkeypatch)`: verify borrowing fails if book does not exist  
  
- **R4_test_return_book.py**
  - `test_return_book_invalid_patron_id(tmp_path, monkeypatch)`: verify returning fails with invalid patron ID
  - `test_return_book_not_found(tmp_path, monkeypatch)`: verify returning fails if book does not exist
  - `test_return_book_not_borrowed(tmp_path, monkeypatch)`: verify returning fails if patron never borrowed the book
  - `test_return_book_valid(tmp_path, monkeypatch)`: verify returning succeeds for borrowed book  
  
- **R5_test_late_fee.py**
  - `test_late_fee_no_overdue(tmp_path, monkeypatch)`: verify no late fee if book is returned before due date
  - `test_late_fee_within_seven_days(tmp_path, monkeypatch)`: verify late fee within a week overdue
  - `test_late_fee_beyond_seven_Days(tmp_path, monkeypatch)`: verify late fee beyond a week overdue
  - `test_late_fee_maximum_cap(tmp_path, monkeypatch)`: verify late fee cap ($15.00)
  - `test_late_fee_book_not_borrowed(tmp_path, monkeypatch)`: verify no fee for patron who didn't borrow a book  
  
- **R6_test_book_search.py**
  - `test_search_books_by_title(verify no fee for patron who didn't borrow a book)`: verify searching by valid title
  - `test_search_books_by_author(tmp_path, monkeypatch)`: verify searching by valid author
  - `test_serach_books_by_isbn(tmp_path, monkeypatch)`: verify searching by ISBN (exact match)
  - `test_search_books_no_results(tmp_path, monkeypatch)`: verify searching returns empty list if no matches found
  - `test_serach_books_invalid_Type(tmp_path, monkeypatch)`: verify searching with invalid search type returns empty list  
  
- **R7_test_patron_status.py**
  - `test_patron_status_invalid_id(tmp_path, monkeypatch)`: verify report returns error for invlid patron ID
  - `test_patron_status_no_loans(tmp_path, monkeypatch)`: verify report shows no loans and no fees if patron has borrowed nothing
  - `test_patron_status_with_current_loan(tmp_path, monkeypatch)`: verify report includes a currently borrowed book
  - `test_patron_status_with_late_fee(tmp_path, monkeypatch)`: verify report calculates late fees for patron correctly
  - `test_patron_status_history_includes_records`: verify borrwing history is recorded  
