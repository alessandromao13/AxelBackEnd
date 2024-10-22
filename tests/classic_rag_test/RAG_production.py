import os
import pdfplumber
from pathlib import Path
from unstructured.partition.pdf import partition_pdf


def extract_tables_with_pdfplumber(content_path, file_to_read):
    # Convert to Path object
    full_path = Path(content_path) / file_to_read
    print(f"Reading from: {full_path} using pdfplumber")
    got_tables = []
    try:
        with pdfplumber.open(full_path) as pdf:  # Ensure full_path is a valid Path object
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                if page_tables:
                    got_tables.extend(page_tables)
                    print(f"Found {len(page_tables)} tables on page {page_num + 1}")
    except Exception as e:
        print(f"An error occurred while extracting tables: {e}")

    return got_tables


def doc_partition(content_path, file_to_read):
    full_path = os.path.join(content_path, file_to_read)
    print(f"Reading from: {full_path}")

    try:
        raw_pdf_elems = partition_pdf(filename=full_path)

    except Exception as e:
        print(f"An error occurred while partitioning the PDF: {e}")
        return []

    return raw_pdf_elems


def data_category(raw_pdf_elems):
    data_tables = []
    data_texts = []

    for element in raw_pdf_elems:
        print(f"Processing element of type: {element.__class__.__name__}")

        element_type = element.__class__.__name__

        if element_type == "Table":
            data_tables.append(str(element))
        elif element_type in ["Text", "NarrativeText", "CompositeElement", "ListItem"]:
            data_texts.append(str(element))
        elif element_type == "Title":
            data_texts.append(str(element))
        else:
            print(f"Skipping unknown element type: {element_type}")

    return data_texts, data_tables


if __name__ == '__main__':
    path = "./"
    file_name = "Temporizzatori.pdf"
    print("EXTRACTING RAW ELEMENTS")
    raw_pdf_elements = doc_partition(path, file_name)
    texts, _ = data_category(raw_pdf_elements)
    print("TEXTS:", texts)
    tables = extract_tables_with_pdfplumber(path, file_name)
    print("TABLES:", tables)
