# backend.py
import time

def perform_task(data):
    """Simulates backend processing."""
    time.sleep(2)  # Simulating a delay
    return f"Processed data: {data.upper()}"
