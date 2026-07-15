# SpendSave Backend (Flask + SQLite)

*Save Smarter. Spend Wiser.*

The **SpendSave Backend** powers the SpendSave web application by handling transaction management, automatic spare-change savings, spending analytics, and savings goals. Built with **Flask** and **SQLite**, it is designed as a lightweight backend for a single-user demo or academic project.

---

## Project Structure

```
backend/
├── app.py              # Flask application and API routes
├── requirements.txt    # Python dependencies
└── README.md           # Backend documentation
```

> **Note:** A SQLite database (`spendsave.db`) is automatically created when the application is run for the first time.

---

## Requirements

- Python 3.10+
- Flask
- Flask-CORS
- SQLite (included with Python)

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## Running the Backend

Start the Flask server by running:

```bash
python app.py
```

The backend will start at:

```
http://127.0.0.1:5000
```

---

## Features

- Add and manage transactions
- Automatic round-up savings calculation
- Spending analytics by category
- Dashboard summary
- Savings goal management
- RESTful API
- SQLite database integration

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/transactions` | Retrieve all transactions |
| POST | `/api/transactions` | Add a new transaction |
| DELETE | `/api/transactions/<id>` | Delete a transaction |
| GET | `/api/summary` | Get spending and savings summary |
| GET | `/api/analytics` | View category-wise spending analytics |
| GET | `/api/goal` | Retrieve the current savings goal |
| POST | `/api/goal` | Update the savings goal |

---

## Round-Up Savings Logic

Every transaction is automatically rounded up to the nearest **₹10**.

The difference between the actual amount and the rounded value is saved as spare change.

**Example**

| Transaction | Rounded To | Saved |
|-------------|------------|-------|
| ₹63 | ₹70 | ₹7 |
| ₹145.50 | ₹150 | ₹4.50 |
| ₹899.30 | ₹900 | ₹0.70 |

This accumulated spare change is displayed in the SpendSave dashboard.

---

## Technologies Used

- Python
- Flask
- Flask-CORS
- SQLite

---

## Future Enhancements

- User Authentication
- Bank API Integration
- AI-Based Spending Insights
- Budget Planning
- Cloud Database Support
- Email Notifications
