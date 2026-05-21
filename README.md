# CRM Epic Events

A command-line CRM application for managing clients, contracts, and events for Epic Events, a company specializing in event organization.

---

## Table of Contents

- [Description](#description)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Commands](#available-commands)

---

## Description

CRM Epic Events is a CLI application built with Python following an MVC architecture. It allows three types of users (sales, support, management) to manage collaborators, customers, contracts, and events with role-based access control.

---

## Tech Stack

- **Python 3.14**
- **PostgreSQL** — database
- **Peewee** — ORM
- **Click** — CLI framework
- **JWT** — authentication
- **Argon2** — password hashing
- **Sentry** — error monitoring
- **uv** — dependency management

---

## Installation

### Prerequisites

- Python 3.14+
- PostgreSQL
- uv

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/CRM_EPIC-EVENTS.git
cd CRM_EPIC-EVENTS
```

**2. Install dependencies**

```bash
uv sync
```

**3. Create the database**

```bash
psql -U your_username -d postgres -c "CREATE DATABASE database_epic_events;"
```

---

## Configuration

**1. Create a `.env` file at the root of the project**

```bash
DATABASE=database_epic_events
USER=your_postgres_username
PASSWORD=your_postgres_password
HOST=localhost
PORT=5432
JWT_SECRET=your_jwt_secret_key
DSN_SENTRY=your_sentry_dsn
```

**2. Run the migrations**

```bash
pw_migrate migrate --directory src/migrations --database postgresql://your_username@localhost:5432/database_epic_events
```

---

## Usage

**Launch the application**

```bash
python main.py --help
```

**Create a first management user directly in the database**

```bash
psql -U your_username -d database_epic_events
```

```sql
INSERT INTO users (name, password, role) VALUES ('Admin', 'hashed_password', 'management');
```

**Login**

```bash
python main.py login --user_id 1 --password your_password
```

---

## Available Commands

### Authentication

| Command | Description |
|---|---|
| `login` | Log in and get a token |
| `logout` | Log out |
| `check-token` | Check the current token |

### Collaborators (Users)

| Command | Description | Role |
|---|---|---|
| `create-user` | Create a new collaborator | management |
| `get-user-by-id` | Get a collaborator by ID | all |
| `update-user-information` | Update a collaborator | management |
| `delete-user-by-id` | Delete a collaborator | management |

### Contracts

| Command | Description | Role |
|---|---|---|
| `create-contract` | Create a new contract | management |
| `get-contract-by-id` | Get a contract by ID | all |
| `update-contract` | Update a contract | management, sales |
| `delete-contract-by-id` | Delete a contract | management |
| `filter-contract` | Filter contracts by status | all |
| `filter-contract-by-remaining-paid` | Filter unpaid contracts | all |

### Events

| Command | Description | Role |
|---|---|---|
| `create-event` | Create a new event | sales |
| `get-event-by-id` | Get an event by ID | all |
| `update-event` | Update an event | sales, support, management |
| `delete-event` | Delete an event | sales |
| `filter-event-by-contact` | Filter events by support contact | all |
| `filter-event-without-support` | Filter events without support | all |
| `assign-support-contact` | Assign a support contact to an event | management |

### Customers

| Command | Description | Role |
|---|---|---|
| `create-customer` | Create a new customer | sales |
| `update-customer` | Update a customer | sales |
| `delete-customer` | Delete a customer | sales |

---

## Roles & Permissions

| Permission | management | sales | support |
|---|---|---|---|
| Create collaborator | ✅ | ❌ | ❌ |
| Update collaborator | ✅ | ❌ | ❌ |
| Delete collaborator | ✅ | ❌ | ❌ |
| Create contract | ✅ | ❌ | ❌ |
| Update contract | ✅ | ✅ | ❌ |
| Create event | ❌ | ✅ | ❌ |
| Update event | ✅ | ✅ | ✅ |
| Assign support | ✅ | ❌ | ❌ |
| Create customer | ❌ | ✅ | ❌ |
| Update customer | ❌ | ✅ | ❌ |