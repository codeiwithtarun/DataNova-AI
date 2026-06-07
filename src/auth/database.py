import sqlite3

# DATABASE CONNECTION
conn = sqlite3.connect("users.db", check_same_thread=False)

cursor = conn.cursor()

# =========================================
# USERS TABLE
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# =========================================
# HISTORY TABLE
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    action TEXT
)
""")

conn.commit()
# =========================================
# CLEANED DATASETS TABLE
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS cleaned_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    dataset_name TEXT
)
""")

conn.commit()

# =========================================
# CREATE USER
# =========================================

def create_user(email, password):

    try:

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        conn.commit()

        return True

    except:

        return False

# =========================================
# LOGIN USER
# =========================================

def login_user(email, password):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    return user

# =========================================
# SAVE HISTORY
# =========================================

def save_history(email, action):

    cursor.execute(
        "INSERT INTO history (email, action) VALUES (?, ?)",
        (email, action)
    )

    conn.commit()

# =========================================
# GET HISTORY
# =========================================

def get_history(email):

    cursor.execute(
        "SELECT action FROM history WHERE email=?",
        (email,)
    )

    return cursor.fetchall()

# =========================================
# DATABASE LOADED
# =========================================

print("Database loaded successfully")
# =========================================
# SAVE CLEANED DATASET
# =========================================

def save_cleaned_dataset(email, dataset_name):

    cursor.execute(
        "INSERT INTO cleaned_datasets (email, dataset_name) VALUES (?, ?)",
        (email, dataset_name)
    )

    conn.commit()


# =========================================
# GET CLEANED DATASETS
# =========================================

def get_cleaned_datasets(email):

    cursor.execute(
        "SELECT dataset_name FROM cleaned_datasets WHERE email=? ORDER BY id DESC LIMIT 5",
        (email,)
    )

    return cursor.fetchall()