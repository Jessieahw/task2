# import os
# import re

# def beautify_text(content):
#     """
#     Beautifies the raw content by removing unnecessary headers, footers, and formatting artifacts.
#     """
#     # Remove multiple spaces and newlines
#     content = re.sub(r'\s+', ' ', content).strip()
    
#     # Remove page numbers and other extraneous formatting
#     content = re.sub(r'Page\s+\d+', '', content, flags=re.IGNORECASE)
    
#     # Normalize spacing around punctuation
#     content = re.sub(r'\s*([.,:;!?])\s*', r'\1 ', content)
    
#     # Add line breaks for readability (after sections, headings, etc.)
#     content = re.sub(r'(Item\s+\d+\.\s+[A-Za-z ]+)', r'\n\1\n', content, flags=re.IGNORECASE)
    
#     return content

# def extract_items(content, accession_number):
#     """
#     Extracts individual items (e.g., Item 1, Item 7) and their content from the filing.
#     Saves each item as a separate file.
#     """
#     # Regular expression to find items and their content
#     item_pattern = re.compile(r'(Item\s+\d+[^:]*:\s*.*?)(?=Item\s+\d+|$)', re.IGNORECASE | re.DOTALL)
    
#     matches = item_pattern.findall(content)
#     if not matches:
#         print(f"No items found in the filing for {accession_number}.")
#         return
    
#     for match in matches:
#         # Extract item title and content
#         title_match = re.match(r'Item\s+\d+[^:]*:\s*(.*?)$', match.strip(), re.IGNORECASE)
#         title = title_match.group(1).strip() if title_match else "Unknown"
        
#         # Beautify the content
#         beautified_content = beautify_text(match)
        
#         # Save to a file
#         filename = f"{accession_number} ({title}).txt"
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(beautified_content)
#         print(f"Saved: {filename}")

# def process_filing(file_path):
#     """
#     Processes a raw filing file: beautifies content and extracts individual items.
#     """
#     accession_number = os.path.splitext(os.path.basename(file_path))[0]
    
#     with open(file_path, 'r', encoding='utf-8') as f:
#         content = f.read()
    
#     # Beautify the entire content
#     beautified_content = beautify_text(content)
    
#     # Save the beautified full filing
#     beautified_file = f"{accession_number} (Beautified).txt"
#     with open(beautified_file, 'w', encoding='utf-8') as f:
#         f.write(beautified_content)
#     print(f"Saved beautified filing: {beautified_file}")
    
#     # Extract and save items
#     extract_items(beautified_content, accession_number)

# # Example Usage:
# # Replace with the actual path to the downloaded filing
# filing_path = "/Users/jessie/Downloads/task2/8K_files/0001770787-24-000004.txt"
# process_filing(filing_path)




# import re

# def beautify_text(raw_text):
#     """
#     Cleans and formats the input raw text to make it more readable.
#     """
#     # Remove unnecessary markers or escape sequences
#     cleaned_text = re.sub(r'&#160;', ' ', raw_text)  # Replace non-breaking spaces
#     cleaned_text = re.sub(r'&#\d+;', '', cleaned_text)  # Remove HTML entities like &#8220;
#     cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  # Remove HTML tags
#     cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Standardize whitespace
#     return cleaned_text

# def extract_item_content(beautified_text, item_names):
#     """
#     Extracts the content for each item based on the list of item names.
#     """
#     item_contents = {}
#     for i, current_item in enumerate(item_names):
#         # Determine the stopping point: the name of the next item or end of document
#         next_item = item_names[i + 1] if i + 1 < len(item_names) else None

#         # Build regex pattern for the current item
#         if next_item:
#             pattern = re.compile(
#                 rf"(Item\s\d+\.\d+\s{re.escape(current_item)}.*?)(?=Item\s\d+\.\d+\s{re.escape(next_item)})",
#                 re.DOTALL
#             )
#         else:
#             # Last item: extract until the end of the document
#             pattern = re.compile(
#                 rf"(Item\s\d+\.\d+\s{re.escape(current_item)}.*)",
#                 re.DOTALL
#             )
        
#         # Extract the content for the current item
#         match = pattern.search(beautified_text)
#         if match:
#             item_contents[current_item] = match.group(1).strip()
#         else:
#             item_contents[current_item] = f"Content for '{current_item}' not found."

#     return item_contents

# def process_text_file(input_file_path, beautified_file_path, output_dir, item_info_list):
#     """
#     Beautifies the text, extracts specified item contents, and saves results.
#     """
#     try:
#         # Read the input file
#         with open(input_file_path, 'r', encoding='utf-8') as file:
#             raw_text = file.read()
        
#         # Step 1: Beautify the text
#         beautified_text = beautify_text(raw_text)
        
#         # Save beautified text
#         with open(beautified_file_path, 'w', encoding='utf-8') as file:
#             file.write(beautified_text)
        
#         print(f"Beautified text saved to {beautified_file_path}")
        
#         # Step 2: Extract contents for each item
#         extracted_contents = extract_item_content(beautified_text, item_info_list)
        
#         # Step 3: Save each item's content
#         for item_name, content in extracted_contents.items():
#             sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name)  # Sanitize file name
#             output_file_path = f"{output_dir}/{sanitized_item_name}.txt"
#             with open(output_file_path, 'w', encoding='utf-8') as file:
#                 file.write(content)
#             print(f"Extracted content for '{item_name}' saved to {output_file_path}")
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example Usage
# if __name__ == "__main__":
#     # Input and output paths
#     input_file = "/Users/jessie/Downloads/task2/8K_files/0001770787-24-000004.txt"  # Input file containing raw text
#     beautified_file = "/Users/jessie/Downloads/task2/8K_files/beautified_file.txt"  # File to save beautified text
#     output_directory = "/Users/jessie/Downloads/task2/8K_files"  # Directory to save extracted contents
    
#     # List of ITEM INFORMATION names from the file
#     item_info = [
#         "Results of Operations and Financial Condition",
#         "Financial Statements and Exhibits"
#     ]
    
#     # Process the file
#     process_text_file(input_file, beautified_file, output_directory, item_info)




# # not well
# import re
# import os

# def extract_items(content):
#     """
#     Extracts items and their contents from the provided text content.
#     """
#     # Regular expression to match item titles (e.g., "Item 9.01")
#     item_pattern = re.compile(r"(Item\s\d+\.\d+.*?)</span>", re.DOTALL)
    
#     # Regular expression to match the end ID (e.g., <div id="i22a9f44407a64fb3a6f5d9eccb84774c_13"></div>)
#     end_id_pattern = re.compile(r'<div id="i[\w\d]+"></div>')

#     # Find all item titles
#     items = item_pattern.finditer(content)
    
#     extracted_items = []

#     for item in items:
#         start_index = item.start()
#         # Find the next matching ID after the current item
#         end_id_match = end_id_pattern.search(content, start_index)
#         end_index = end_id_match.start() if end_id_match else len(content)

#         # Extract content of the current item
#         item_content = content[start_index:end_index]
#         title = item.group(1).strip()
#         extracted_items.append((title, item_content))
    
#     return extracted_items

# def beautify_content(content):
#     """
#     Beautifies content by removing HTML tags and extra spaces.
#     """
#     # Remove HTML tags and unnecessary spaces
#     clean_content = re.sub(r"<[^>]*>", "", content)
#     clean_content = re.sub(r"\s+", " ", clean_content)
#     return clean_content.strip()
# def save_items_to_files(items, output_dir="extracted_items"):
#     """
#     Saves extracted items to individual text files, ensuring filenames are not too long.
#     """
#     # Ensure output directory exists
#     os.makedirs(output_dir, exist_ok=True)

#     for idx, (title, content) in enumerate(items, start=1):
#         # Beautify content
#         clean_content = beautify_content(content)

#         # Clean title for filename
#         sanitized_title = re.sub(r"[^\w\s]", "_", title)  # Remove invalid characters
#         truncated_title = (sanitized_title[:100] + "...") if len(sanitized_title) > 100 else sanitized_title
#         filename = f"Item_{idx}_{truncated_title}.txt"  # Ensure unique filenames
        
#         file_path = os.path.join(output_dir, filename)
        
#         # Save to file
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(f"{title}\n\n{clean_content}")
#         print(f"Saved: {file_path}")

# # Example usage
# input_file = "/Users/jessie/Downloads/task2/8K_files/0001770787-24-000004.txt"  # Input file containing raw text

# with open(input_file, "r", encoding="utf-8") as f:
#     content = f.read()

# # Extract, beautify, and save items
# extracted_items = extract_items(content)
# save_items_to_files(extracted_items)


# # work, try dynamically

# import re
# import os

# def beautify_text(raw_text):
#     """
#     Cleans and formats the input raw text to make it more readable.
#     """
#     # Remove unnecessary markers or escape sequences
#     cleaned_text = re.sub(r'&#160;', ' ', raw_text)  # Replace non-breaking spaces
#     cleaned_text = re.sub(r'&#\d+;', '', cleaned_text)  # Remove HTML entities like &#8220;
#     cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  # Remove HTML tags
#     cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Standardize whitespace
#     return cleaned_text

# def extract_item_content(beautified_text, item_names):
#     """
#     Extracts the content for each item based on the list of item names.
#     Skips extraction for "Financial Statements and Exhibits".
#     """
#     item_contents = {}
#     for i, current_item in enumerate(item_names):
#         # Skip extraction for "Financial Statements and Exhibits"
#         if current_item == "Financial Statements and Exhibits":
#             continue

#         # Determine the stopping point: the name of the next item or end of document
#         next_item = item_names[i + 1] if i + 1 < len(item_names) else None

#         # Build regex pattern for the current item
#         if next_item:
#             pattern = re.compile(
#                 rf"(Item\s\d+\.\d+\s{re.escape(current_item)}.*?)(?=Item\s\d+\.\d+\s{re.escape(next_item)})",
#                 re.DOTALL
#             )
#         else:
#             # Last item: extract until the end of the document
#             pattern = re.compile(
#                 rf"(Item\s\d+\.\d+\s{re.escape(current_item)}.*)",
#                 re.DOTALL
#             )

#         # Extract the content for the current item
#         match = pattern.search(beautified_text)
#         if match:
#             item_contents[current_item] = match.group(1).strip()
#         else:
#             item_contents[current_item] = f"Content for '{current_item}' not found."

#     return item_contents

# def process_text_file(input_file_path, beautified_file_path, output_dir, item_info_list):
#     """
#     Beautifies the text, extracts specified item contents (excluding specific items), and saves results.
#     """
#     try:
#         # Read the input file
#         with open(input_file_path, 'r', encoding='utf-8') as file:
#             raw_text = file.read()

#         # Step 1: Beautify the text
#         beautified_text = beautify_text(raw_text)

#         # Save beautified text
#         with open(beautified_file_path, 'w', encoding='utf-8') as file:
#             file.write(beautified_text)

#         print(f"Beautified text saved to {beautified_file_path}")

#         # Step 2: Extract contents for each item
#         extracted_contents = extract_item_content(beautified_text, item_info_list)

#         # Step 3: Save each item's content
#         for item_name, content in extracted_contents.items():
#             sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name)  # Sanitize file name
#             output_file_path = os.path.join(output_dir, f"{sanitized_item_name}.txt")
#             with open(output_file_path, 'w', encoding='utf-8') as file:
#                 file.write(content)
#             print(f"Extracted content for '{item_name}' saved to {output_file_path}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example Usage
# if __name__ == "__main__":
#     # Input and output paths
#     input_file = "/Users/jessie/Downloads/task2/8K_files/0001770787-24-000004.txt"  # Input file containing raw text
#     beautified_file = "/Users/jessie/Downloads/task2/8K_files/beautified_file.txt"  # File to save beautified text
#     output_directory = "/Users/jessie/Downloads/task2/8K_files"  # Directory to save extracted contents

#     # List of ITEM INFORMATION names from the file
#     item_info = [
#         "Results of Operations and Financial Condition",
#         "Financial Statements and Exhibits"
#     ]

#     # Process the file
#     process_text_file(input_file, beautified_file, output_directory, item_info)


# no working well

# import re
# import os

# def beautify_text(raw_text):
#     """
#     Cleans and formats the input raw text to make it more readable.
#     """
#     # Remove unnecessary markers or escape sequences
#     cleaned_text = re.sub(r'&#160;', ' ', raw_text)  # Replace non-breaking spaces
#     cleaned_text = re.sub(r'&#\d+;', '', cleaned_text)  # Remove HTML entities like &#8220;
#     cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  # Remove HTML tags
#     cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Standardize whitespace
#     return cleaned_text

# def extract_item_names(raw_text):
#     """
#     Extracts item names from lines starting with "ITEM INFORMATION:".
#     """
#     items = []
#     for line in raw_text.splitlines():
#         if line.startswith("ITEM INFORMATION:"):
#             items.append(line.split("ITEM INFORMATION:")[1].strip())
#     print(items)
#     return items

# def extract_item_content(beautified_text, item_names):
#     """
#     Extracts the content for each item based on the list of item names.
#     Skips extraction for "Financial Statements and Exhibits".
#     """
#     item_contents = {}
#     for i, current_item in enumerate(item_names):
#         # Skip extraction for "Financial Statements and Exhibits"
#         if current_item == "Financial Statements and Exhibits":
#             continue

#         # Determine the stopping point: the name of the next item or end of document
#         next_item = item_names[i + 1] if i + 1 < len(item_names) else None

#         # Build regex pattern for the current item
#         if next_item:
#             pattern = re.compile(
#                 rf"(Item\\s\\d+\\.\\d+\\s{re.escape(current_item)}.*?)(?=Item\\s\\d+\\.\\d+\\s{re.escape(next_item)})",
#                 re.DOTALL
#             )
#         else:
#             # Last item: extract until the end of the document
#             pattern = re.compile(
#                 rf"(Item\\s\\d+\\.\\d+\\s{re.escape(current_item)}.*)",
#                 re.DOTALL
#             )

#         # Extract the content for the current item
#         match = pattern.search(beautified_text)
#         if match:
#             item_contents[current_item] = match.group(1).strip()
#         else:
#             item_contents[current_item] = f"Content for '{current_item}' not found."

#     return item_contents

# def process_text_file(input_file_path, beautified_file_path, output_dir):
#     """
#     Beautifies the text, extracts specified item contents (excluding specific items), and saves results.
#     """
#     try:
#         # Read the input file
#         with open(input_file_path, 'r', encoding='utf-8') as file:
#             raw_text = file.read()

#         # Step 1: Extract item names
#         item_info_list = extract_item_names(raw_text)

#         # Step 2: Beautify the text
#         beautified_text = beautify_text(raw_text)

#         # Save beautified text
#         with open(beautified_file_path, 'w', encoding='utf-8') as file:
#             file.write(beautified_text)

#         print(f"Beautified text saved to {beautified_file_path}")

#         # Step 3: Extract contents for each item
#         extracted_contents = extract_item_content(beautified_text, item_info_list)

#         # Step 4: Save each item's content
#         for item_name, content in extracted_contents.items():
#             sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name)  # Sanitize file name
#             output_file_path = os.path.join(output_dir, f"{sanitized_item_name}.txt")
#             with open(output_file_path, 'w', encoding='utf-8') as file:
#                 file.write(content)
#             print(f"Extracted content for '{item_name}' saved to {output_file_path}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example Usage
# if __name__ == "__main__":
#     # Input and output paths
#     input_file = "/Users/jessie/Downloads/task2/8K_files/0001770787-24-000004.txt"  # Input file containing raw text
#     beautified_file = "/Users/jessie/Downloads/task2/8K_files/beautified_file.txt"  # File to save beautified text
#     output_directory = "/Users/jessie/Downloads/task2/8K_files"  # Directory to save extracted contents

#     # Process the file
#     process_text_file(input_file, beautified_file, output_directory)


# not well

# import re
# import os

# def beautify_text(raw_text):
#     """
#     Cleans and formats the input raw text to make it more readable.
#     """
#     # Remove unnecessary markers or escape sequences
#     cleaned_text = re.sub(r'&#160;', ' ', raw_text)  # Replace non-breaking spaces
#     cleaned_text = re.sub(r'&#\d+;', '', cleaned_text)  # Remove HTML entities like &#8220;
#     cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  # Remove HTML tags
#     cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Standardize whitespace
#     return cleaned_text

# def normalize_text(text):
#     """
#     Normalizes text by removing or replacing certain punctuation marks.
#     """
#     return re.sub(r'[;:,.]', '', text).strip()

# def extract_item_names(raw_text):
#     """
#     Extracts item names from lines starting with "ITEM INFORMATION:".
#     """
#     items = []
#     for line in raw_text.splitlines():
#         if line.startswith("ITEM INFORMATION:"):
#             items.append(line.split("ITEM INFORMATION:")[1].strip())
    
#     return items

# def extract_accession_number(raw_text):
#     """
#     Extracts the accession number from the raw text.
#     """
#     match = re.search(r'ACCESSION NUMBER:\s*(\d{10}-\d{2}-\d{6})', raw_text)
#     if match:
#         return match.group(1)
#     return "Unknown_Accession"

# def extract_item_content(beautified_text, item_names):
#     """
#     Extracts the content for each item based on the list of item names.
#     Skips extraction for "Financial Statements and Exhibits".
#     """
#     item_contents = {}
#     for i, current_item in enumerate(item_names):
#         # Skip extraction for "Financial Statements and Exhibits"
#         if current_item == normalize_text("Financial Statements and Exhibits"):
#             continue

#         # Determine the stopping point: the name of the next item or end of document
#         next_item = item_names[i + 1] if i + 1 < len(item_names) else None

#         # Build regex pattern for the current item
#         current_item_pattern = normalize_text(current_item)
#         next_item_pattern = normalize_text(next_item) if next_item else None

#         if next_item_pattern:
#             pattern = re.compile(
#                 rf"(Item\s\d+\s{re.escape(normalize_text(current_item))}.*?)(?=Item\s\d+\.\d+\s{re.escape(normalize_text(next_item_pattern))})",
#                 re.IGNORECASE | re.DOTALL
#             )

#         else:
#             # Last item: extract until the end of the document
#             pattern = re.compile(
#                 rf"(Item\s\d+\s{re.escape(normalize_text(current_item))}.*)",
#                 re.DOTALL | re.IGNORECASE
#             )

#         # Extract the content for the current item
#         print(pattern)
#         normalized_text = normalize_text(beautified_text)
#         # print(beautified_text)
        

#         match = pattern.search(normalized_text)
        
#         if match:
#             item_contents[current_item] = match.group(1).strip()
#         else:
#             item_contents[current_item] = f"Content for '{current_item}' not found."

#     return item_contents

# def read_file(file_path):
#     """
#     Reads a file with fallback for encoding issues.
#     """
#     encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'windows-1252']
#     for encoding in encodings:
#         try:
#             with open(file_path, 'r', encoding=encoding) as file:
#                 return file.read()
#         except UnicodeDecodeError:
#             continue
#     # If all encodings fail, read as binary and decode ignoring errors
#     with open(file_path, 'rb') as file:
#         return file.read().decode('utf-8', errors='ignore')

# def save_beautified_text(beautified_text, output_file_path):
#     """
#     Saves the beautified text to a specified file path.
#     """
#     try:
#         with open(output_file_path, 'w', encoding='utf-8') as file:
#             file.write(normalize_text(beautified_text))
#         print(f"Beautified text saved to {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred while saving beautified text: {e}")


# def process_text_file(input_file_path, output_dir):
#     """
#     Beautifies the text, extracts specified item contents (excluding specific items), and saves results.
#     """
#     try:
#         for filename in os.listdir(input_file_path):
#             file_path = os.path.join(input_file_path, filename)
#             if not os.path.isfile(file_path):
#                 continue
#             print(file_path)
#             # Read the input file
#             raw_text = read_file(file_path)

#             # Extract the accession number
#             accession_number = extract_accession_number(raw_text)


#             items = extract_item_names(raw_text)

#             # Step 1: Beautify the text
#             beautified_text = beautify_text(raw_text)
#             beautified_file_path = os.path.join(output_dir, f"{accession_number}_beautified.txt")
#             save_beautified_text(beautified_text, beautified_file_path)


#             # Step 2: Extract contents for each item
#             extracted_contents = extract_item_content(beautified_text, items)

#             # Step 3: Save each item's content
#             for item_name, content in extracted_contents.items():
#                 sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name)  # Sanitize file name
#                 # output_file_path = os.path.join(output_dir, f"{sanitized_item_name}.txt")
#                 output_file_name = f"{accession_number} ({sanitized_item_name}).txt"
#                 output_file_path = os.path.join(output_dir, output_file_name)

#                 with open(output_file_path, 'w', encoding='utf-8') as file:
#                     file.write(content)


            
                    

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example Usage
# if __name__ == "__main__":
#     # Input and output paths
#     input_file = "/Users/jessie/Downloads/task2/8K_files"  # Input file containing raw text
#     # beautified_file = "/Users/jessie/Downloads/task2/8K_files/beautified_file.txt"  # File to save beautified text
#     output_directory = "/Users/jessie/Downloads/task2/8K_files/output"  # Directory to save extracted contents

#     os.makedirs(output_directory, exist_ok=True)

#     # Process the file
#     process_text_file(input_file, output_directory)


# # good



import re
import os

def beautify_text(raw_text):
    """
    Cleans and formats the input raw text to make it more readable.
    """
    # Remove unnecessary markers or escape sequences
    cleaned_text = re.sub(r'&#160;', ' ', raw_text)  # Replace non-breaking spaces
    cleaned_text = re.sub(r'&#\d+;', '', cleaned_text)  # Remove HTML entities like &#8220;
    cleaned_text = re.sub(r'<.*?>', '', cleaned_text)  # Remove HTML tags
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Standardize whitespace
    return cleaned_text

def normalize_text(text):
    """
    Normalizes text by removing or replacing certain punctuation marks.
    """
    return re.sub(r'[;:,]', '', text).strip()

def extract_item_names(raw_text):
    """
    Extracts item names from lines starting with "ITEM INFORMATION:".
    """
    items = []
    for line in raw_text.splitlines():
        if line.startswith("ITEM INFORMATION:"):
            items.append(line.split("ITEM INFORMATION:")[1].strip())
    
    return items

def extract_accession_number(raw_text):
    """
    Extracts the accession number from the raw text.
    """
    match = re.search(r'ACCESSION NUMBER:\s*(\d{10}-\d{2}-\d{6})', raw_text)
    if match:
        return match.group(1)
    return "Unknown_Accession"

# def save_beautified_text(text, filename="beautified_text.txt"):
#     """
#     Saves the provided beautified text to a file.
#     """
#     with open(filename, "w") as file:
#         file.write(normalize_text(text))

def extract_item_content(beautified_text, item_names):
    """
    Extracts the content for each item based on the list of item names.
    Skips extraction for "Financial Statements and Exhibits".
    """
    item_contents = {}
    date_pattern = re.compile(r"Date:\s\w+\s\d{1,2},\s\d{4}")

    # Search for the date line in the beautified text
    date_match = date_pattern.search(beautified_text)
    if date_match:
        date_position = date_match.start()
        beautified_text = beautified_text[:date_position]

    for i, current_item in enumerate(item_names):
        # Skip extraction for "Financial Statements and Exhibits"
        # print(normalize_text(current_item))
        
        if current_item == normalize_text("Financial Statements and Exhibits"):
            continue

        if normalize_text(current_item) == normalize_text("Departure of Directors or Certain Officers Election of Directors Appointment of Certain Officers Compensatory Arrangements of Certain Officers"):
            hardcoded_content_pattern = re.compile(
                rf"(Item\s\d+\.\d+\sDeparture\ of\ Directors\ or\ Principal\ Officers\ Election\ of\ Directors\ Appointment\ of\ Principal\ Officers.*?)(?=Item\s\d+\.\d+|$)",
                re.DOTALL
            )
            # print("hey")
            match = hardcoded_content_pattern.search(normalize_text(beautified_text))
            # print(match)
            if match:
                
                item_contents[current_item] = match.group(1).strip()
                continue
        # Determine the stopping point: the name of the next item or end of document
        next_item = item_names[i + 1] if i + 1 < len(item_names) else None

        # Build regex pattern for the current item
        current_item_pattern = normalize_text(current_item)
        next_item_pattern = normalize_text(next_item) if next_item else None

        # if next_item_pattern:
        #     pattern = re.compile(
        #         rf"(Item\s\d+\.\d+\s{re.escape(current_item_pattern)}.*?)(?=Item\s\d+\.\d+\s{re.escape(next_item_pattern)})",
        #         re.DOTALL
        #     )
        # else:
        #     # Last item: extract until the end of the document
        #     pattern = re.compile(
        #         rf"(Item\s\d+\.\d+\s{re.escape(current_item_pattern)}.*)",
        #         re.DOTALL
        #     )

        if next_item_pattern:
            pattern = re.compile(
                rf"(Item\s\d+\.\d+\s?{re.escape(current_item_pattern)}.*?)(?=Item\s\d+\.\d+\s?{re.escape(next_item_pattern)})",
                re.DOTALL
            )
        else:
            # Last item: extract until the end of the document
            pattern = re.compile(
                rf"(Item\s\d+\.\d+\s?{re.escape(current_item_pattern)}.*)",
                re.DOTALL
            )

        # Extract the content for the current item
        match = pattern.search(normalize_text(beautified_text))

        if match:
            item_contents[current_item] = match.group(1).strip()
        else:
            item_contents[current_item] = f"Content for '{current_item}' not found."

    return item_contents

def read_file_with_fallback(file_path):
    """
    Reads a file with fallback for encoding issues.
    """
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    # If all encodings fail, read as binary and decode ignoring errors
    with open(file_path, 'rb') as file:
        return file.read().decode('utf-8', errors='ignore')
    
def process_text_file(input_file_path, output_dir):
    """
    Beautifies the text, extracts specified item contents (excluding specific items), and saves results.
    """
    try:
        for filename in os.listdir(input_file_path):
            file_path = os.path.join(input_file_path, filename)
            if not os.path.isfile(file_path):
                continue
            # print(file_path)
            # Read the input file
            raw_text = read_file_with_fallback(file_path)

            # Extract the accession number
            accession_number = extract_accession_number(raw_text)


            items = extract_item_names(raw_text)

            # Step 1: Beautify the text
            beautified_text = beautify_text(raw_text)
            # save_beautified_text(beautified_text)

            # Step 2: Extract contents for each item
            extracted_contents = extract_item_content(beautified_text, items)

            # Step 3: Save each item's content
            for item_name, content in extracted_contents.items():
                sanitized_item_name = re.sub(r'[^a-zA-Z0-9_]', '_', item_name)  # Sanitize file name
                # output_file_path = os.path.join(output_dir, f"{sanitized_item_name}.txt")
                output_file_name = f"{accession_number} ({sanitized_item_name}).txt"
                output_file_path = os.path.join(output_dir, output_file_name)

                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    # Input and output paths
    input_file = "/Users/jessie/Downloads/task2/8K_files"  # Input file containing raw text
    # beautified_file = "/Users/jessie/Downloads/task2/8K_files/beautified_file.txt"  # File to save beautified text
    output_directory = "/Users/jessie/Downloads/task2/8K_files/output"  # Directory to save extracted contents

    os.makedirs(output_directory, exist_ok=True)

    # Process the file
    process_text_file(input_file, output_directory)