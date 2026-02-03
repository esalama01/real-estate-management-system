# 🏡 Real Estate Management System

A comprehensive Real Estate CRM application built with **Python**, **Streamlit**, and **MongoDB**.
This project is designed to help real estate agents manage property listings, potential clients (prospects), and visits efficiently, featuring a dynamic search engine and an agent dashboard.

## 🚀 Features

-   **🏠 Property Management:** Add, list, and view property details (Villas, Apartments, Shops...).
-   **👥 Lead Management:** Register and track potential clients (Prospects).
-   **🤝 Visit Tracking:** Schedule and log visits, linking clients to specific properties.
-   **🔍 Advanced Search Engine:** Dynamic filtering by city, property type, and budget using MongoDB queries.
-   **🔐 Agent Authentication:** Secure login system for authorized agents.
-   **📊 Live Dashboard:** Real-time showcase of the latest opportunities on the homepage.
-   **🎲 Data Generator:** Includes a script (`seeder.py`) to populate the database with realistic fake data for testing.

## 🛠️ Tech Stack

-   **Language:** Python 3.x
-   **Frontend & Backend:** [Streamlit](https://streamlit.io/)
-   **Database:** [MongoDB](https://www.mongodb.com/) (NoSQL)
-   **Libraries:** `pymongo`, `faker`

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/esalama01/real-estate-management-system.git](https://github.com/esalama01/real-estate-management-system.git)
    cd real-estate-management-system
    ```

2.  **Install dependencies**
    Since there is no `requirements.txt`, simply run:
    ```bash
    pip install streamlit pymongo faker
    ```

3.  **Start MongoDB**
    Ensure your local MongoDB instance is running on port `27017`.

4.  **Populate Database (Optional)**
    Generate fake data (ads, clients, visits) to test the app:
    ```bash
    python seeder.py
    ```

5.  **Run the Application**
    ```bash
    streamlit run 1_Homepage.py
    ```

## 📂 Project Structure

```text
📁 real-estate-management-system/
│
├── 📜 1_Homepage.py       # Main Entry Point (Dashboard & Login)
├── 📜 seeder.py           # Fake Data Generator
│
└── 📁 pages/              # App Modules
    ├── 📜 2_Annonce.py    # Property Listings
    ├── 📜 3_Prospect.py   # Client Registration
    ├── 📜 4_Visite.py     # Visit Management
    └── 📜 5_Recherche.py  # Public Search Engine
