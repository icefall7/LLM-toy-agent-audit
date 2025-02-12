import sqlite3
from typing import Dict, Any
import json
import os


class DatabaseManager:
    def __init__(self):
        # Create database directory if it doesn't exist
        os.makedirs('database', exist_ok=True)
        
        # Initialize two separate databases with absolute paths
        db_dir = os.path.join(os.path.dirname(__file__))
        self.db1 = sqlite3.connect(os.path.join(db_dir, 'db1.sqlite'))
        self.db2 = sqlite3.connect(os.path.join(db_dir, 'db2.sqlite'))
        self._init_databases()

    def _init_databases(self):
        """Initialize database tables"""
        # Create tables in both databases
        for db in [self.db1, self.db2]:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    birthday TEXT
                )
            ''')
            db.commit()

    def seed_sample_data(self):
        """Seed databases with sample data"""
        # Sample data for DB1
        db1_data = [
            (123, "aaa@gmail.com", "7347777777", 
             "77 Massachusetts Avenue, Cambridge, MA 02139-4307", "02/11/2025"),
            (124, "bbb@gmail.com", "7341234567", 
             "123 Main St, Ann Arbor, MI 48104", "03/15/1990")
        ]

        # Sample data for DB2 (with some differences)
        db2_data = [
            (123, "aa.a@hotmail.com", "1-734-777-7777", 
             "77 Massachusetts Ave, Cambridge, MA 02139", "02/11/2025"),
            (124, "bbb.work@company.com", "734-123-4567", 
             "123 Main Street, Ann Arbor, MI 48104", "03/15/1990")
        ]

        # Insert data into DB1
        self.db1.executemany(
            'INSERT OR REPLACE INTO user_profiles VALUES (?, ?, ?, ?, ?)',
            db1_data
        )
        self.db1.commit()

        # Insert data into DB2
        self.db2.executemany(
            'INSERT OR REPLACE INTO user_profiles VALUES (?, ?, ?, ?, ?)',
            db2_data
        )
        self.db2.commit()

    def get_profile(self, user_id: int, db_num: int) -> Dict[str, Any]:
        """Get user profile from specified database"""
        db = self.db1 if db_num == 1 else self.db2
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM user_profiles WHERE user_id = ?', 
            (user_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "user_id": row[0],
                "email": row[1],
                "phone": row[2],
                "address": row[3],
                "birthday": row[4]
            }
        return None

    def update_profile(self, profile: Dict[str, Any], db_num: int) -> bool:
        """Update user profile in specified database"""
        db = self.db1 if db_num == 1 else self.db2
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                UPDATE user_profiles 
                SET email = ?, phone = ?, address = ?, birthday = ?
                WHERE user_id = ?
            ''', (
                profile["email"],
                profile["phone"],
                profile["address"],
                profile["birthday"],
                profile["user_id"]
            ))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating database {db_num}: {str(e)}")
            return False 