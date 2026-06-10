# 💱 Streamlit Currency Converter — Financial-Terminal UI

A high-performance, responsive Streamlit currency converter web application styled with a sleek, dark financial-terminal aesthetic. This project features an advanced exchange-rate computation engine, local transaction persistence via atomic line-delimited JSON storage, and a robust test suite powered by `pytest`.

## 🚀 Features

- **Financial-Terminal UI**: Styled with deep tones (`#0f1923`), high-contrast terminal accents (`#00e5ff`), customized table components, and clean typography utilizing *IBM Plex Mono* and *IBM Plex Sans*.
- **Singleton Exchange Engine**: Utilizes a strict singleton API client configuration featuring a pre-compiled high-precision multi-currency matrix.
- **Atomic Operations & Error Handling**: Custom exception hierarchy handling validations (`ValidationError`), upstream issues (`APIConnectionError`), and storage faults (`PersistenceError`).
- **Performance Auditing**: Built-in Python decorators automatically capture, measure, and log operational execution latency down to microsecond thresholds.
- **Local Transaction Persistence**: Appends operations continuously into a flat-file JSON schema, featuring automated reversal for chronological indexing and user-triggered teardowns.
- **Mock-Isolated Test Infrastructure**: Includes an isolated test runner targeting state mutations, validations, edge-case rounding constraints, and structural HTML rendering.

---

## 📂 Architecture & Data Flow

Presentation layers are cleanly decoupled from data handling strategies via network-isolated REST endpoints to prevent framework lock-in and streamline automated testing:

       [ User Interface Layer ]
                  │
                  ▼ (Triggers Conversion / History Views)
       ┌────────────────────────┐
       │   Currency_Converter   │ (Streamlit Frontend Client - Port 8501)
       └───────────┬────────────┘
                   │
                   ▼ (HTTP Network Requests / JSON Data Contracts)
       ┌────────────────────────┐
       │      app_backend       │ (Flask REST API Engine - Port 8000)
       └───────────┬────────────┘
                   │
                   ▼ (Persists Logs / Reads Ledger State)
       ┌────────────────────────┐
       │  history.json Ledger   │ (Flat-File Storage Database)
       └────────────────────────┘
                   ▲
                   │ (Intercepts Network Boundary Assertions)
       ┌───────────┴────────────┐
       │Test_Currency_Converter │ (Pytest Suite with Network Mocking Stubs)
       └────────────────────────┘

## 📦 Directory Manifesto

```text
├── app_backend.py              # Headless Flask REST API Server & Matrix Database
├── Currency_Converter.py       # Stateless Streamlit Presentation & UI Engine
├── Test_Currency_Converter.py  # Comprehensive Pytest Suite with Mocking Stubs
├── history.json                # Atomic Flat-File Database Storage (Auto-generated)
├── requirements.txt            # Unified Package Dependencies Manifest
├── .gitignore                  # Strict Repository Upload Filter File
└── README.md                   # Project System Documentation