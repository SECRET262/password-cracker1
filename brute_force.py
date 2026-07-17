"""
Brute Force Attack Module
Tries all character combinations up to a maximum length
"""

import time
import itertools


class BruteForce:
    def __init__(self, target_password, max_length, charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        """
        Initialize brute force attack
        
        Args:
            target_password: Password to crack
            max_length: Maximum password length to try
            charset: Characters to use in combinations
        """
        self.target_password = target_password
        self.max_length = max_length
        self.charset = charset
        self.attempts = 0
        self.start_time = None
        self.end_time = None
    
    def attack(self):
        """
        Perform brute force attack
        
        Returns:
            dict with success info or None if failed
        """
        self.start_time = time.time()
        
        # Try all lengths from 1 to max_length
        for length in range(1, self.max_length + 1):
            print(f"  Trying length {length}...")
            
            # Generate all combinations of current length
            for combination in itertools.product(self.charset, repeat=length):
                password = ''.join(combination)
                self.attempts += 1
                
                # Show progress every 10000 attempts
                if self.attempts % 10000 == 0:
                    print(f"  Attempts: {self.attempts}...", end='\r')
                
                if password == self.target_password:
                    self.end_time = time.time()
                    return {
                        'password': password,
                        'attempts': self.attempts,
                        'time': self.end_time - self.start_time
                    }
        
        self.end_time = time.time()
        return {
            'password': None,
            'attempts': self.attempts,
            'time': self.end_time - self.start_time
        }