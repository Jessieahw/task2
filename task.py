# # The code below will download the required files (form of "8-k", specific CIK, specific year).
# And then it will extract the required infomation (Accession Number, Conformed submission type, Conformed period of report, Filed as of Date, Company Conformed Name, Item Information).
# Files will be saved into a folder called 8K-files and output will be saved as 8K_extracted_data.csv.

# To run the code, you may consider checking your browser's User-Agent using the link provided in the email first (line33 and line 70).

import os
import pandas as pd
import requests
import time


form = "8-K"
CIKs = [1770787, 1770787, 1495648]
begyear, endyear = 2023, 2024
quarters = [ "QTR1","QTR2", "QTR3","QTR4"]
base_url = "https://www.sec.gov/Archives/"
output_dir = "8K_files" 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

columns = ["Accession Number", "Conformed Submission Type", "Conformed Period of Report",
           "Filed As Of Date", "Company Conformed Name", "Item Information 1", "Item Information 2"]
df = pd.DataFrame(columns=columns)

# Function to parse each form.idx file
def parse_form_idx(quarter):
    idx_url = f"{base_url}edgar/full-index/2024/{quarter}/form.idx"
    
    # May consider changing to your browser's User-Agent 
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
    }
    
    response = requests.get(idx_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {idx_url}. Status Code: {response.status_code}")
        return []

    
    
    lines = response.text.splitlines()
    results = []

    for line in lines:
        if form not in line:
            continue

        parts = line.split()
        cik = int(parts[-3]) if len(parts) > 2 else None
        
        if cik in CIKs:
            file_url = base_url + parts[-1]
            download_txt_file(file_url)

            file_path = os.path.join(output_dir, os.path.basename(file_url))
            extracted_data = extract_data_from_txt(file_path)

            results.append(extracted_data)

    return results

# Function to download the .txt file
def download_txt_file(url):

    # May consider changing to your browser's User-Agent
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
    }
    
    response = requests.get(url, headers=headers, allow_redirects=True)
    
    if response.status_code == 200:
        file_path = os.path.join(output_dir, os.path.basename(url))
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url} - Status Code: {response.status_code}")

# Function to extract the required data from each .txt file
def extract_data_from_txt(file_path):
    data = {"Accession Number": "", "Conformed Submission Type": "", "Conformed Period of Report": "",
            "Filed As Of Date": "", "Company Conformed Name": "", "Item Information 1": "", "Item Information 2": ""}
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    accession_number = content.split("ACCESSION NUMBER:")[1].split("\n")[0].strip()
    submission_type = content.split("CONFORMED SUBMISSION TYPE:")[1].split("\n")[0].strip()
    period_of_report = content.split("CONFORMED PERIOD OF REPORT:")[1].split("\n")[0].strip()
    filed_as_of = content.split("FILED AS OF DATE:")[1].split("\n")[0].strip()
    company_name = content.split("COMPANY CONFORMED NAME:")[1].split("\n")[0].strip()

    data["Accession Number"] = accession_number
    data["Conformed Submission Type"] = submission_type
    data["Conformed Period of Report"] = period_of_report
    data["Filed As Of Date"] = filed_as_of
    data["Company Conformed Name"] = company_name

    items = []
    for line in content.splitlines():
        if line.startswith("ITEM INFORMATION:"):
            items.append(line.split("ITEM INFORMATION:")[1].strip())
    
    for i in range(len(items)):
        key = f"Item Information {i + 1}"
        data[key] = items[i]

    return data

# Loop through each quarter and parse the respective form.idx files
for quarter in quarters:
    results = parse_form_idx(quarter)
    df = pd.concat([df, pd.DataFrame(results)], ignore_index=True)

# Save the dataframe to a CSV file
df.to_csv("8K_extracted_data.csv", index=False)

print("Data extraction completed and saved to '8K_extracted_data.csv'.")
