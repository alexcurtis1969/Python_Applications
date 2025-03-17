# Pull Request: Add Basic Toll Booth Management System

**Description:**

This pull request introduces a basic toll booth management system implemented in Python. It includes a `TollBooth` class for processing toll transactions, generating daily reports, and a utility function for generating sample data.

**Changes:**

* Added `TollBooth` class:
    * Implements `__init__` for initializing toll booths with ID and rate.
    * Implements `process_toll` for recording transactions.
    * Implements `generate_daily_report` for generating daily summaries.
* Added `generate_sample_data` function:
    * Generates random toll transactions for testing.
* Added example usage in the main section of the `toll_booth.py` script.
* Added a `README.md` file with instructions, features, and further enhancements.

**Motivation:**

This system provides a foundational structure for managing toll transactions, which can be extended to include more advanced features like database integration, electronic toll collection, and real-time reporting.

**Testing:**

* The included sample data generation and daily report generation functionality have been tested.
* Manual inspection of the generated reports confirms accurate calculations.

**Checklist:**

* [x] Code follows project coding standards.
* [x] Code is properly documented.
* [x] Changes are tested and working.
* [x] `README.md` is updated with relevant information.

**Potential Improvements (Future PRs):**

* Database integration for persistent storage of transactions.
* Implementation of electronic toll collection (ETC) functionality.
* Real-time reporting and dashboard features.
* Addition of unit tests.
* Addition of lane management.
* Addition of time of day tolling.
* Addition of vehicle specific tolling.

**Files Changed:**

* `toll_booth.py`
* `README.md`

**Screenshots (if applicable):**
(If you have any relevant screenshots of the output, include them here.)