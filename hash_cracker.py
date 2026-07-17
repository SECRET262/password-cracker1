"""
Hash Cracker Module
Cracks hashes (MD5, SHA1, SHA256) using dictionary attack
"""

import time
import hashlib


class HashCracker:
    def __init__(self, hash_type, target_hash, wordlist_file):
        """
        Initialize hash cracker
        
        Args:
            hash_type: Type of hash (md5, sha1, sha256)
            target_hash: Hash value to crack
            wordlist_file: Path to wordlist file
        """
        self.hash_type = hash_type.lower()
        self.target_hash = target_hash.lower()
        self.wordlist_file = wordlist_file
        self.attempts = 0
        self.start_time = None
        self.end_time = None
    
    def hash_password(self, password):
        """
        Hash a password using specified hash type
        
        Args:
            password: Password to hash
            
        Returns:
            Hashed password as hex string
        """
        if self.hash_type == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif self.hash_type == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif self.hash_type == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported hash type: {self.hash_type}")
    
    def attack(self):
        """
        Perform hash cracking attack
        
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
                    
                    # Hash the password and compare
                    password_hash = self.hash_password(password)
                    
                    if password_hash == self.target_hash:
                        self.end_time = time.time()
                        return {
                            'password': password,
                            'hash': password_hash,
                            'attempts': self.attempts,
                            'time': self.end_time - self.start_time
                        }
        
        except FileNotFoundError:
            print(f"Error: Wordlist file '{self.wordlist_file}' not found!")
            return None
        
        self.end_time = time.time()
        return {
            'password': None,
            'hash': None,
            'attempts': self.attempts,
            'time': self.end_time - self.start_time
        }