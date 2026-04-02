# 💰 Python Based Finance System Backend

A clean, structured Flask backend for managing personal financial records — built as part of the Python Developer Intern assignment.

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flask 3.0 |
| Database | SQLite (via SQLAlchemy ORM) |
| Language | Python 3.10+ |
| API Style | REST API (JSON) |

---

## 📁 Project Structure

```
finance_system/
├── app.py                     # App factory, blueprint registration
├── config.py                  # Configuration (DB URI, secret key)
├── extensions.py              # SQLAlchemy instance
├── requirements.txt
│
├── models/
│   ├── user.py                # User model (roles: viewer, analyst, admin)
│   └── transaction.py         # Transaction model (income/expense)
│
├── services/
│   ├── transaction_service.py # Business logic: CRUD + validation
│   ├── summary_service.py     # Analytics: totals, categories, monthly
│   └── user_service.py        # User creation and role management
│
├── routes/
│   ├── transactions.py        # /api/transactions endpoints
│   ├── summary.py             # /api/summary endpoints
│   └── users.py               # /api/users endpoints
│
└── utils/
    ├── role_guard.py          # Role-based access decorator
    └── seed.py                # Sample data on first run
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd finance_system
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

The server will start at: `http://127.0.0.1:5000`

> On first run, the database is auto-created and seeded with sample users and transactions.

---

## 🔐 Role-Based Access

Roles are passed via the `X-User-Role` request header.

| Role | Permissions |
|---|---|
| `viewer` | View transactions and basic summary |
| `analyst` | View + filter + create/edit transactions, access detailed analytics |
| `admin` | Full access including delete and user management |

**Example header:**
```
X-User-Role: admin
```

> Note: In a production system, this would be handled via JWT tokens or session auth. For this assignment, role simulation via headers keeps the focus on backend structure and business logic.

---

## 📡 API Reference

### Transactions — `/api/transactions`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/` | all | List all transactions (filterable) |
| GET | `/<id>` | all | Get single transaction |
| POST | `/` | analyst, admin | Create new transaction |
| PUT | `/<id>` | analyst, admin | Update transaction |
| DELETE | `/<id>` | admin | Delete transaction |

**Filter query params (GET /):**
```
?type=expense
?category=Groceries
?user_id=1
?date_from=2025-01-01&date_to=2025-03-31
```

**POST body example:**
```json
{
  "amount": 5000,
  "type": "expense",
  "category": "Rent",
  "date": "2025-04-01",
  "user_id": 1,
  "notes": "April rent payment"
}
```

---

### Summary & Analytics — `/api/summary`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/` | all | Overview: income, expenses, balance |
| GET | `/categories` | analyst, admin | Category-wise breakdown |
| GET | `/monthly` | analyst, admin | Monthly income/expense/net |
| GET | `/recent` | all | Recent transactions (default: last 5) |

**Example response — GET /api/summary/**
```json
{
  "total_income": 105000.0,
  "total_expenses": 7500.0,
  "current_balance": 97500.0,
  "total_transactions": 8
}
```

---

### Users — `/api/users`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/` | admin | List all users |
| GET | `/<id>` | all | Get user by ID |
| POST | `/` | admin | Create new user |
| PUT | `/<id>` | admin | Update user / change role |
| DELETE | `/<id>` | admin | Delete user |

---

## ✅ Validation & Error Handling

All endpoints return appropriate HTTP status codes:

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request / missing JSON body |
| 403 | Permission denied (wrong role) |
| 404 | Resource not found |
| 422 | Validation error (invalid data) |

**Validation includes:**
- Amount must be a positive number
- Type must be `income` or `expense`
- Date must be in `YYYY-MM-DD` format
- User must exist before creating a transaction
- Email must be unique when creating users
- Role changes restricted to admin only

---

## 📊 Sample Data (Auto-Seeded)

| User | Email | Role |
|---|---|---|
| Abhay Admin | admin@finance.com | admin |
| Riya Analyst | riya@finance.com | analyst |
| Raj Viewer | raj@finance.com | viewer |

Sample transactions include salary, groceries, rent, freelance income, and entertainment entries across March–April 2025.

---

## 💡 Assumptions Made

1. **Role via header** — Role-based access is simulated using the `X-User-Role` header. A production system would use JWT authentication.
2. **SQLite** — Chosen for simplicity and portability. The ORM layer (SQLAlchemy) makes switching to PostgreSQL/MySQL trivial by changing one line in `config.py`.
3. **No password hashing** — User model does not include passwords since authentication is out of scope for this assignment.
4. **Soft assumptions on fields** — `notes` is optional. All other transaction fields are required.

---

## 🧪 Quick Test (using curl)

```bash
# Get summary (all roles)
curl http://localhost:5000/api/summary/

# Create a transaction (analyst/admin only)
curl -X POST http://localhost:5000/api/transactions/ \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -d '{"amount": 2000, "type": "expense", "category": "Utilities", "date": "2025-04-10", "user_id": 1}'

# Get monthly breakdown (analyst/admin only)
curl -H "X-User-Role: analyst" http://localhost:5000/api/summary/monthly

# Delete a transaction (admin only)
curl -X DELETE http://localhost:5000/api/transactions/1 \
  -H "X-User-Role: admin"
```

---

## 👤 Author

**Abhay Likhar**
Python Developer Intern Assignment — Zorvyn Screening Portal
