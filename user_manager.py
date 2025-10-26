import json
import os
from datetime import datetime
from threading import Lock

class UserManager:
    def __init__(self, file_path='users.json'):
        self.file_path = file_path
        self.lock = Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
    
    def _read_users(self):
        with self.lock:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    print(f"[DEBUG] Read {len(data)} users from database")
                    return data
            except Exception as e:
                print(f"[ERROR] Failed to read users: {e}")
                return {}
    
    def _write_users(self, users):
        with self.lock:
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(users, f, indent=2)
                print(f"[DEBUG] Wrote {len(users)} users to database")
            except Exception as e:
                print(f"[ERROR] Failed to write users: {e}")
    
    def is_registered(self, user_id):
        users = self._read_users()
        return str(user_id) in users
    
    def register_user(self, user_id, username, first_name, last_name=None):
        users = self._read_users()
        user_id_str = str(user_id)
        
        if user_id_str not in users:
            users[user_id_str] = {
                'user_id': user_id,
                'username': username or 'N/A',
                'first_name': first_name or 'N/A',
                'last_name': last_name or 'N/A',
                'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_checks': 0,
                'is_premium': False
            }
            self._write_users(users)
            return True
        return False
    
    def get_user(self, user_id):
        users = self._read_users()
        user_data = users.get(str(user_id))
        print(f"[DEBUG] Getting user {user_id}: {user_data is not None}")
        if user_data and 'is_premium' not in user_data:
            print(f"[DEBUG] Adding is_premium field to user {user_id}")
            user_data['is_premium'] = False
            users[str(user_id)] = user_data
            self._write_users(users)
        return user_data
    
    def set_premium(self, user_id, is_premium=True):
        users = self._read_users()
        user_id_str = str(user_id)
        
        if user_id_str in users:
            users[user_id_str]['is_premium'] = is_premium
            self._write_users(users)
            return True
        return False
    
    def is_premium(self, user_id):
        user_data = self.get_user(user_id)
        if user_data:
            return user_data.get('is_premium', False)
        return False
    
    def update_user_checks(self, user_id):
        users = self._read_users()
        user_id_str = str(user_id)
        
        if user_id_str in users:
            users[user_id_str]['total_checks'] += 1
            self._write_users(users)
    
    def get_total_users(self):
        users = self._read_users()
        return len(users)
