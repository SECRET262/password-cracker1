#!/usr/bin/env python3
"""
Password Cracker - A multi-method password cracking tool
Supports: Dictionary attacks, Brute force, Hash cracking
"""

import sys
import time
from dictionary_attack import DictionaryAttack
from brute_force import BruteForce
from hash_cracker import HashCracker


def main():
    print("=" * 60)
    print("PASSWORD CRACKER v1.0")
    print("=" * 60)
    print("\nSelect attack method:")
    print("1. Dictionary Attack (fast, common passwords)")
    print("2. Brute Force (slow, try all combinations)")
    print("3. Hash Cracker (MD5, SHA1, SHA256)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        dictionary_attack()
    elif choice == "2":
        brute_force_attack()
    elif choice == "3":
        hash_attack()
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice!")
        main()


def dictionary_attack():
    """Run dictionary attack"""
    target = input("Enter target password to crack: ").strip()
    wordlist_file = input("Enter wordlist file path (default: wordlists/common.txt): ").strip()
    
    if not wordlist_file:
        wordlist_file = "wordlists/common.txt"
    
    print(f"\nStarting dictionary attack on: {target}")
    print(f"Using wordlist: {wordlist_file}\n")
    
    attacker = DictionaryAttack(target, wordlist_file)
    result = attacker.attack()
    
    if result:
        print(f"\n✓ SUCCESS! Password found: {result['password']}")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")
    else:
        print(f"\n✗ FAILED! Password not found in wordlist")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")


def brute_force_attack():
    """Run brute force attack"""
    target = input("Enter target password to crack: ").strip()
    max_length = int(input("Enter maximum password length (default: 4): ") or "4")
    charset = input("Enter character set (default: abc123): ").strip() or "abc123"
    
    print(f"\nStarting brute force attack on: {target}")
    print(f"Max length: {max_length}, Charset: {charset}\n")
    
    attacker = BruteForce(target, max_length, charset)
    result = attacker.attack()
    
    if result:
        print(f"\n✓ SUCCESS! Password found: {result['password']}")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")
    else:
        print(f"\n✗ FAILED! Could not crack password")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")


def hash_attack():
    """Run hash cracking attack"""
    print("\nSupported hash types: MD5, SHA1, SHA256")
    hash_type = input("Enter hash type (md5/sha1/sha256): ").strip().lower()
    hash_value = input("Enter hash to crack: ").strip()
    wordlist_file = input("Enter wordlist file path (default: wordlists/common.txt): ").strip()
    
    if not wordlist_file:
        wordlist_file = "wordlists/common.txt"
    
    print(f"\nStarting hash crack ({hash_type})...")
    print(f"Hash: {hash_value}\n")
    
    cracker = HashCracker(hash_type, hash_value, wordlist_file)
    result = cracker.attack()
    
    if result:
        print(f"\n✓ SUCCESS! Password found: {result['password']}")
        print(f"Hash: {result['hash']}")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")
    else:
        print(f"\n✗ FAILED! Password not found in wordlist")
        print(f"Attempts: {result['attempts']}")
        print(f"Time: {result['time']:.2f} seconds")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
