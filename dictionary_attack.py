"""
Dictionary Attack Module
Tries passwords from a wordlist file
"""

import time


class DictionaryAttack:
    def __init__(self, target_password, wordlist_file):
        """
        Initialize dictionary attack
        
        Args:
            target_password: Password to crack
            wordlist_file: Path to wordlist file
        """
        self.target_password = target_password
        self.wordlist_file = wordlist_file
        self.attempts = 0
        self.start_time = None
        self.end_time = None
    
    def attack(self):
        """
        Perform dictionary attack
        
        Returns:
            dict with success info or None if failed
        """
        self.start_time = time.time()
        
        try:
            with open(self.wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    self.attempts += 1
                    
                    # Show progress every 1000 attempts
                    if self.attempts % 1000 == 0:
                        print(f"  Attempts: {self.attempts}...", end='\r')
                    
                    if password == self.target_password:
                        self.end_time = time.time()
                        return {
                            'password': password,
                            'attempts': self.attempts,
                            'time': self.end_time - self.start_time
                        }
        
        except FileNotFoundError:
            print(f"Error: Wordlist file '{self.wordlist_file}' not found!")
            return None
        
        self.end_time = time.time()
        return {
            'password': None,
            'attempts': self.attempts,
            'time': self.end_time - self.start_time
        }