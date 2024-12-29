"""
This code will beautify, extract and save the contents of each item.

Changing to your corresponding directory will be needed before running the code (line 130 and 131).

Item named "Financial Statements and Exhibits" will be ignored. 
Comment line 61 and 62, and then the code will extract "Financial Statements and Exhibits" as well.
But it's not working well sometimes as it's hard to determine the endpoint for this item.

This code will be run in a folder containing all text files that need to be processed. 
The outputs will be saved in a folder called "output" in the same directory as the text files

The "output" directory will have all the contents of items. Each file will be named as "accession number (item name).txt" 

"""


import re
import os

# Function to clean and format the input raw text.
def beautify_text(raw_text):
    cleaned_text = re.sub(r'&#160;', ' ', raw_text) 
    cleaned_text = re.sub(r'&#\d+;', '', cleaned_text) 
    cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  
    return cleaned_text

# Funtion to remove certain punctuation marks.
def normalize_text(text):
    return re.sub(r'[;:,]', '', text).strip()


# Funtion to extract item names
def extract_item_names(raw_text):
    items = []
    for line in raw_text.splitlines():
        if line.startswith("ITEM INFORMATION:"):
            items.append(line.split("ITEM INFORMATION:")[1].strip())
    
    return items

# Funtion to extract accession number
def extract_accession_number(raw_text):
    match = re.search(r'ACCESSION NUMBER:\s*(\d{10}-\d{2}-\d{6})', raw_text)
    if match:
        return match.group(1)
    return "Unknown_Accession"

# Funtion to extract item contents except for "Financial Statements and Exhibits"
def extract_item_content(beautified_text, item_names):
    item_contents = {}
    date_pattern = re.compile(r"Date:\s\w+\s\d{1,2},\s\d{4}")
    date_match = date_pattern.search(beautified_text)
    if date_match:
        date_position = date_match.start()
        beautified_text = beautified_text[:date_position]
    for i, current_item in enumerate(item_names):

        # comment the following two lines, ant then the code will extract "Financial Statements and Exhibits" as well, but it's not working well sometimes as it's hard to determine the endpoint for this item.
        if current_item == normalize_text("Financial Statements and Exhibits"):
            continue

        if normalize_text(current_item) == normalize_text("Departure of Directors or Certain Officers Election of Directors Appointment of Certain Officers Compensatory Arrangements of Certain Officers"):
            hardcoded_content_pattern = re.compile(
                rf"(Item\s\d+\.\d+\sDeparture\ of\ Directors\ or\ Principal\ Officers\ Election\ of\ Directors\ Appointment\ of\ Principal\ Officers.*?)(?=Item\s\d+\.\d+|$)",
                re.DOTALL
            )
            match = hardcoded_content_pattern.search(normalize_text(beautified_text))
            if match:
                item_contents[current_item] = match.group(1).strip()
                continue
        next_item = item_names[i + 1] if i + 1 < len(item_names) else None
        current_item_pattern = normalize_text(current_item)
        next_item_pattern = normalize_text(next_item) if next_item else None
        if next_item_pattern:
            pattern = re.compile(
                rf"(Item\s\d+\.\d+\s?{re.escape(current_item_pattern)}.*?)(?=Item\s\d+\.\d+\s?{re.escape(next_item_pattern)})",
                re.DOTALL
            )
        else:
            pattern = re.compile(
                rf"(Item\s\d+\.\d+\s?{re.escape(current_item_pattern)}.*)",
                re.DOTALL
            )
        match = pattern.search(normalize_text(beautified_text))
        if match:
            item_contents[current_item] = match.group(1).strip()
        else:
            item_contents[current_item] = f"Content for '{current_item}' not found."
    return item_contents

# Funtion to read files
def read_file_with_fallback(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    with open(file_path, 'rb') as file:
        return file.read().decode('utf-8', errors='ignore')
    
# Funtion to beautify, extract and save the item contents
def process_text_file(input_file_path, output_dir):
    try:
        for filename in os.listdir(input_file_path):
            file_path = os.path.join(input_file_path, filename)
            if not os.path.isfile(file_path):
                continue
            raw_text = read_file_with_fallback(file_path)
            accession_number = extract_accession_number(raw_text)
            items = extract_item_names(raw_text)
            beautified_text = beautify_text(raw_text)
            extracted_contents = extract_item_content(beautified_text, items)
            for item_name, content in extracted_contents.items():
                sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name) 
                output_file_name = f"{accession_number} ({sanitized_item_name}).txt"
                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    # Change to your directory
    input_file = "/Users/jessie/Downloads/task2/8K_files" 
    output_directory = "/Users/jessie/Downloads/task2/8K_files/output"  

    os.makedirs(output_directory, exist_ok=True)
    process_text_file(input_file, output_directory)