import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from uuid import uuid4

# Function to extract all linked pages
def find_linked_pages(url):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    links = soup.find_all('a', href=True)
    linked_pages = set()
    for link in links:
        href = link['href']
        if href.startswith('https://www.apexon.com/resources/case-studies/'):
            linked_pages.add(href)
    
    return list(linked_pages)

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        header = soup.find('header')
        if header:
            header.decompose()
        
        footer = soup.find('footer')
        if footer:
            footer.decompose()
        
        page_text = soup.get_text(separator=' ', strip=True)
        return page_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {url}: {e}")
        return None

def app():
    st.title('Web Scraping and Data Preprocessing Tool')
    main_url = st.text_input("Enter the main URL to scrape:", value="https://www.apexon.com/success-stories/")
    
    if st.button("Start Scraping and Processing"):
        if main_url:
            # Extract and print linked URLs
            linked_urls = find_linked_pages(main_url)
            texts = []
            urls = []
            
            for url in linked_urls:
                text = extract_text_from_url(url)
                if text:
                    urls.append(url)
                    # Remove specified phrases
                    phrases_to_remove = [
                        """This website uses cookies to offer you the best experience online...""",
                        """More AddThis Share options..."""
                    ]
                    for phrase in phrases_to_remove:
                        text = text.replace(phrase, '')
                    texts.append(text)
            
            # Save to CSV
            filename = f"linked_urls_and_cleaned_content_{str(uuid4())}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['URL', 'Cleaned Text'])
                for url, text in zip(urls, texts):
                    csvwriter.writerow([url, text])
            
            st.success(f"Data has been successfully stored into {filename}")

if __name__ == "__main__":
    app()
