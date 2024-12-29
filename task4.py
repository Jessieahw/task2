import os
import requests

# Constants
form = "10-K"
# quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
quarters = ["QTR1", "QTR2"]
base_url = "https://www.sec.gov/Archives/"
output_dir = "10K_files"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to download the .idx file for a quarter
def download_idx_file(quarter):
    idx_url = f"{base_url}edgar/full-index/2024/{quarter}/form.idx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
    }
    
    response = requests.get(idx_url, headers=headers)
    
    if response.status_code == 200:
        lines = response.text.splitlines()
        for line in lines:
            if form not in line:
                continue

            parts = line.split()
            file_url = base_url + parts[-1]
            download_txt_file(file_url)
    else:
        print(f"Failed to retrieve {idx_url} - Status Code: {response.status_code}")

# Function to download the .txt file
def download_txt_file(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
    }
    
    response = requests.get(url, headers=headers, allow_redirects=True)
    
    if response.status_code == 200:
        file_path = os.path.join(output_dir, os.path.basename(url))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {url} - Status Code: {response.status_code}")

# Loop through each quarter and download relevant files
for quarter in quarters:
    download_idx_file(quarter)

print("Download complete.")
