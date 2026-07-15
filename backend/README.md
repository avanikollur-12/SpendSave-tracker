# SpendSave Backend (Flask + SQLite)

*Save Smarter. Spend Wiser.*

Backend for the **SpendSave** web application that automatically rounds up transactions into savings and provides spending analytics. Built using **Flask** and **SQLite**, this backend is designed for a single-user demo or academic project without authentication.

---

## Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

The frontend can be accessed through Flask or by opening the frontend separately if it is stored in a different folder.

---

## Database

A SQLite database named **spendsave.db** is created automatically the first time the application runs.

Delete the database file anytime if you want to reset all transactions and start fresh.

---

## API Reference

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/transactions` | Retrieve all transactions (latest first) |
| POST | `/api/transactions` | Add a new transaction `{description, amount, category}` |
| DELETE | `/api/transactions/<id>` | Delete a transaction |
| GET | `/api/summary` | Returns `{total_spent, total_saved, transaction_count}` |
| GET | `/api/analytics` | Returns spending grouped by category |
| GET | `/api/goal` | Retrieve current savings goal |
| POST | `/api/goal` | Update savings goal |

---

## Round-Up Savings Logic

SpendSave automatically rounds every transaction up to the nearest **₹10**.

The difference between the transaction amount and the rounded amount is stored as the user's savings.

**Example**

```
Purchase: ₹63
Rounded To: ₹70
Savings: ₹7
```

This spare change is accumulated and displayed in the Savings Dashboard.

---

## Features

- Automatic Round-Up Savings
- Transaction Management
- Spending Analytics
- Savings Summary
- Savings Goal Tracking
- SQLite Database Storage
- RESTful API

---

## Project Structure

```
backend/
├── app.py               # Flask application and API routes
├── requirements.txt     # Python dependencies
├── spendsave.db         # SQLite database (auto-generated)
├── static/
│   └── index.html       # Frontend (if served by Flask)
└── README.md
```

---

## Technologies Used

- Python
- Flask
- SQLite
- REST API

---

## Future Enhancements

- User Authentication
- Bank API Integration
- AI-Based Spending Recommendations
- Monthly Budget Planning
- Cloud Database Support
- Email Notifications
