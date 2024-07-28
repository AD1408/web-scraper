import tkinter as tk
from tkinter import scrolledtext
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import ssl
from urllib.parse import urlparse

# Function to check SSL certificate
def check_ssl(url):
    try:
        parsed_url = urlparse(url)
        context = ssl.create_default_context()
        with context.wrap_socket(ssl.SSLSocket(), server_hostname=parsed_url.netloc) as s:
            s.connect((parsed_url.netloc, 443))
            cert = s.getpeercert()
        return "SSL Verified"
    except Exception as e:
        return f"SSL Verification Failed: {e}"

# Function to perform web scraping and SSL checking
def perform_search():
    query = entry.get()
    results_box.delete(1.0, tk.END)
    
    try:
        for url in search(query, num_results=10):
            ssl_status = check_ssl(url)
            results_box.insert(tk.END, f"URL: {url}\nSSL Status: {ssl_status}\n\n")
            
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results_box.insert(tk.END, f"Title: {soup.title.string}\n\n")
    except Exception as e:
        results_box.insert(tk.END, f"An error occurred: {e}\n")

# Set up GUI
root = tk.Tk()
root.title("Web Scraper with SSL Checker")

tk.Label(root, text="Enter Google Dorking Query:").pack(pady=5)
entry = tk.Entry(root, width=80)
entry.pack(pady=5)

tk.Button(root, text="Search", command=perform_search).pack(pady=10)

results_box = scrolledtext.ScrolledText(root, width=100, height=30)
results_box.pack(pady=10)

root.mainloop()
