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

Presentation layers are cleanly decoupled from data handling strategies to prevent framework lock-in and streamline automated testing:

```text
       [ User Interaction Layer ]
                  │
                  ▼ (Triggers Actions)
       ┌──────────────────────┐
       │ Currency_Converter   │◄───► [ Local State Cache ]
       └──────────┬───────────┘
                  │
                  ├──────────────────────────────┐
                  ▼ (Computes Rates)             ▼ (Persists Logs)
       ┌──────────────────────┐       ┌──────────────────────┐
       │ Singleton Exchange   │       │ history.json Ledger  │
       └──────────────────────┘       └──────────────────────┘
                  ▲                              ▲
                  │ (Verifies Assertions)        │ (Validates IO)
       ┌──────────┴──────────────────────────────┴──────────┐
       │             Test_Currency_Converter.py             │
       └────────────────────────────────────────────────────┘

       ├── Currency_Converter.py       # Main Streamlit Application & UI Engine
├── Test_Currency_Converter.py  # Comprehensive Pytest Test Suite with Mock Stubs
├── .gitignore                  # Strict Repository Upload Filter File
├── requirements.txt            # Unified Package Dependencies Manifest
└── README.md                   # Project System Documentation