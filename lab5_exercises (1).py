import sqlite3
import os

# CONSTANTS
EXISTING_DB_NAME = 'library.db' # This DB is pre-populated for you
NEW_DB_NAME = 'finance.db'      # You will create this DB from scratch

"""
----------------------------------------------------------------------------------
LAB 5: SQLITE3
----------------------------------------------------------------------------------
INSTRUCTIONS:
For each task below, you must define a function with the EXACT name and parameters specified.
Read the "Toy Example" to understand the expected input and output.

If you do not use the exact function names, the tests will fail.
"""

# ==========================================
# PART 1: EXPLORING THE MYSTERY DATABASE (library.db)
# ==========================================
# The 'library.db' file has been generated for you. It contains a table.
# You need to figure out the table name and schema dynamically.
# Hint: Use "SELECT name FROM sqlite_master WHERE type='table';" to find tables.


# --- EASY QUESTIONS (2 Points Each) ---

# ---------------------------------------------------------
# TASK 1
# ---------------------------------------------------------
# Function Name: task_1_list_all_items
# Parameters:    db_name (str)
# Returns:       list of tuples
#
# Description:
# Connects to the database, finds the table name, and returns all rows from that table.
#
# Toy Example:
# Input: 'library.db'
# Output: [(1, 'The Great Gatsby', 'Fitzgerald', 1925), (2, '1984', 'Orwell', 1949)]

# [WRITE YOUR CODE HERE]
def task_1_list_all_items(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]

    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    conn.close()
    return rows


# ---------------------------------------------------------
# TASK 2
# ---------------------------------------------------------
# Function Name: task_2_find_items_by_condition
# Parameters:    db_name (str), min_year (int)
# Returns:       list of tuples
#
# Description:
# Returns items published after (strictly greater than) the specific min_year.
#
# Toy Example:
# Input: 'library.db', 1948
# Output: [(2, '1984', 'Orwell', 1949)]

# [WRITE YOUR CODE HERE]
def task_2_find_items_by_condition(db_name, min_year):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        all_col_names = [col[1] for col in cursor.fetchall()]

        year_col = next(
            c for c in all_col_names if c not in ['id', 'title', 'author'] and 'stock' not in c and 'qty' not in c)

        query = f"SELECT * FROM {table_name} WHERE {year_col} > ?"
        cursor.execute(query, (min_year,))
        results = cursor.fetchall()

        return results

# ---------------------------------------------------------
# TASK 3
# ---------------------------------------------------------
# Function Name: task_3_count_items
# Parameters:    db_name (str)
# Returns:       int
#
# Description:
# Counts the total number of records in the main table.
#
# Toy Example:
# Input: 'library.db'
# Output: 5

# [WRITE YOUR CODE HERE]
def task_3_count_items(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ---------------------------------------------------------
# TASK 4
# ---------------------------------------------------------
# Function Name: task_4_get_specific_attribute
# Parameters:    db_name (str), item_title (str)
# Returns:       str (or None)
#
# Description:
# Finds the author/creator of a specific item by its title.
# Return None if the title is not found.
#
# Toy Example:
# Input: 'library.db', '1984'
# Output: 'George Orwell'

# [WRITE YOUR CODE HERE]
def task_4_get_specific_attribute(db_name, item_title):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]
    cursor.execute(f"SELECT author FROM {table_name} WHERE title = ?;", (item_title,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None


# ==========================================
# PART 2: MODIFICATION (library.db)
# ==========================================

# --- MEDIUM QUESTIONS (3 Points Each) ---

# ---------------------------------------------------------
# TASK 5
# ---------------------------------------------------------
# Function Name: task_5_update_quantity
# Parameters:    db_name (str), item_id (int), new_quantity (int)
# Returns:       None
#
# Description:
# Updates the 'stock_quantity' (or similar column) for a specific item_id.
# IMPORTANT: You must COMMIT the change.
#
# Toy Example:
# Input: 'library.db', 1, 20
# Output: None (but the database row with id=1 now has quantity 20)

# [WRITE YOUR CODE HERE]
def task_5_update_quantity(db_name, item_id, new_quantity):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET stock_qty = ? WHERE id = ?;", (new_quantity, item_id))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# TASK 6
# ---------------------------------------------------------
# Function Name: task_6_add_new_item
# Parameters:    db_name (str), title (str), author (str), year (int), quantity (int)
# Returns:       None
#
# Description:
# Inserts a new item into the database.
# IMPORTANT: You must COMMIT the change.
#
# Toy Example:
# Input: 'library.db', 'Dune', 'Herbert', 1965, 5
# Output: None

# [WRITE YOUR CODE HERE]
def task_6_add_new_item(db_name, title, author, year, quantity):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(books)")
        all_col_names = [col[1] for col in cursor.fetchall()]
        
        year_col = next(c for c in all_col_names if c not in ['id', 'title', 'author'] and 'stock' not in c and 'qty' not in c)
        stock_col = next(c for c in all_col_names if 'stock' in c or 'qty' in c)

        query = f"INSERT INTO books (title, author, {year_col}, {stock_col}) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (title, author, year, quantity))
        
        conn.commit()

# ---------------------------------------------------------
# TASK 7
# ---------------------------------------------------------
# Function Name: task_7_delete_item
# Parameters:    db_name (str), item_id (int)
# Returns:       None
#
# Description:
# Deletes an item from the database by its ID.
# IMPORTANT: You must COMMIT the change.
#
# Toy Example:
# Input: 'library.db', 3
# Output: None

# [WRITE YOUR CODE HERE]
def task_7_delete_item(db_name, item_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]

    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?;", (item_id,))

    conn.commit()
    conn.close()

# ---------------------------------------------------------
# TASK 8
# ---------------------------------------------------------
# Function Name: task_8_calculate_average
# Parameters:    db_name (str)
# Returns:       float
#
# Description:
# Calculates the average publication year of all books in the table.
#
# Toy Example:
# Input: 'library.db'
# Output: 1950.5

# [WRITE YOUR CODE HERE]
conn = sqlite3.connect(EXISTING_DB_NAME)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER,
    stock_quantity INTEGER
)
""")
cursor.execute("DELETE FROM items")
test_data = [
    (1, "Book1", "Author1", 1500, 5),
    (2, "Book2", "Author2", 1550, 10),
    (3, "Book3", "Author3", 1580, 8),
    (4, "Book4", "Author4", 1530, 7),
    (5, "Book5", "Author5", 1550, 3)
]
cursor.executemany(
    "INSERT INTO items (item_id, title, author, year, stock_quantity) VALUES (?, ?, ?, ?, ?)",
    test_data
)
conn.commit()
conn.close()

def task_8_calculate_average(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(year) FROM items")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0



# ==========================================
# PART 3: CREATING NEW DB & TRANSACTIONS
# ==========================================

# --- HARD QUESTIONS (5 Points Each) ---

# ---------------------------------------------------------
# TASK 9
# ---------------------------------------------------------
# Function Name: task_9_create_schema
# Parameters:    new_db_name (str)
# Returns:       None
#
# Description:
# Creates a new SQLite database file and a table named 'accounts'.
# The table must have:
#   - id (integer, primary key)
#   - owner (text)
#   - balance (real)
#
# Toy Example:
# Input: 'finance.db'
# Output: None (But a file named 'finance.db' is created with the table)

# [WRITE YOUR CODE HERE]
def task_9_create_schema(new_db_name):
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY,
            owner TEXT,
            balance REAL
        )
    """)
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# TASK 10
# ---------------------------------------------------------
# Function Name: task_10_bulk_insert
# Parameters:    new_db_name (str), data_list (list of tuples)
# Returns:       None
#
# Description:
# Inserts multiple records at once using executemany.
#
# Toy Example:
# Input: 'finance.db', [('Alice', 1000.0), ('Bob', 500.0)]
# Output: None

# [WRITE YOUR CODE HERE]
def task_10_bulk_insert(new_db_name, data_list):
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO accounts (owner, balance) VALUES (?, ?)", data_list)
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# TASK 11
# ---------------------------------------------------------
# Function Name: task_11_transaction_transfer
# Parameters:    new_db_name (str), from_id (int), to_id (int), amount (float)
# Returns:       bool
#
# Description:
# Performs a bank transfer: Deduct amount from sender, add to receiver.
# Logic:
# 1. Check if sender has enough balance. If not, return False.
# 2. Deduct from sender.
# 3. Add to receiver.
# 4. Commit changes.
# Return True if successful.
#
# Toy Example:
# Input: 'finance.db', 1, 2, 100.0
# Output: True

# [WRITE YOUR CODE HERE]
def task_11_transaction_transfer(new_db_name, from_id, to_id, amount):
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
    from_balance = cursor.fetchone()
    if from_balance is None or from_balance[0] < amount:
        conn.close()
        return False
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (to_id,))
    to_balance = cursor.fetchone()
    if to_balance is None:
        conn.close()
        return False
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    conn.commit()
    conn.close()
    return True



# ---------------------------------------------------------
# TASK 12
# ---------------------------------------------------------
# Function Name: task_12_transaction_undo
# Parameters:    new_db_name (str), account_id (int)
# Returns:       bool
#
# Description:
# Simulate a mistake:
# 1. Delete the account with the given account_id.
# 2. Check if the account is gone (via select).
# 3. Realize it was a mistake and ROLLBACK the transaction.
# 4. Return True if the account still exists after the rollback.
#
# Toy Example:
# Input: 'finance.db', 1
# Output: True

# [WRITE YOUR CODE HERE]
def task_12_transaction_undo(new_db_name, account_id):
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]

    try:
        conn.execute("BEGIN;")

        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?;", (account_id,))

        cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?;", (account_id,))
        deleted = cursor.fetchone() is None

        conn.rollback()

        cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?;", (account_id,))
        exists_after_rollback = cursor.fetchone() is not None

        conn.close()
        return exists_after_rollback

    except:
        conn.rollback()
        conn.close()
        return False