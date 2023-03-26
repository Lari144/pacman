import sqlite3
import pytest 
import logging


def test_create_tables():
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    
    # Check if customers table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers';")
    result = cursor.fetchone()
    assert result[0] == "customers"
    
    # Check if products table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
    result = cursor.fetchone()
    assert result[0] == "products"
    
    # Check if qr_codes table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='qr_codes';")
    result = cursor.fetchone()
    assert result[0] == "qr_codes"
    
    # Check if locations table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations';")
    result = cursor.fetchone()
    assert result[0] == "locations"
    
    conn.close()