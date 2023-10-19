from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import PyPDF2,math

def cut_pdf(pdf_path, subject, start_page, end_page=None):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        if end_page is None:
            end_page = num_pages
        
        folder_name = subject.replace("/", "_")  # Replace any "/" in the subject name with "_"
        # print(pdf_path)
        extract_path = os.path.join("extracts", folder_name)
        # print(extract_path)
        folder_path = os.path.join(os.path.dirname(pdf_path), extract_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
       
        base_dir=os.path.dirname(pdf_path)
        rel_path = os.path.relpath(pdf_path, base_dir)

        base_name=rel_path.replace('\\', '_').replace(' ', '_')
        new_file_name=base_name[:-4]+"_"+subject+".pdf"
        new_file_path = os.path.join(folder_path, new_file_name)
        
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[0])
        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        with open(new_file_path, 'wb') as new_file:
            pdf_writer.write(new_file)


def get_subjects(pdf_path):
    page_numbers = []
    prev=1
    curr=0
    prev_sub=None
    subject=[]
    for page_layout in extract_pages(pdf_path):
        page_number = page_layout.pageid
        found_subject = False
            
        Exceptions=['Correct option changed.','Option 1 is correct.','Option 3 is incorrect.','Aptitude','Programme Feedback',"Group I"]
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    try:
                        x = len(text_line.get_text().strip())
                        count = 0
                        for character in text_line:
                            if isinstance(character, LTChar) and math.ceil(character.size) == 18 and text_line.get_text().strip() not in Exceptions:
                                count += 1
                                # print("sasaa")
                                # print(text_line.get_text().strip())
                            
                        if count == x and count > 0:
                            found_subject = True
                            # print("saaa", text_line.get_text())
                            subject.append(text_line.get_text().strip())
                            
                    except Exception as e:
                        pass
        if found_subject :
            page_numbers.append(page_number)


    return page_numbers,subject



import os

def split_pdf_and_rename(path):
    page_numbers,subject = get_subjects(path)
    for i in range(len(page_numbers)+1):
        if i>0 and i<len(page_numbers):
            cut_pdf(path, subject[i-1], page_numbers[i-1], page_numbers[i])
        if i>=len(page_numbers):
            cut_pdf(path, subject[i-1], page_numbers[i-1]) 
import csv        
def get_subjects_from_folder(folder_path):
    all_subjects = set()
    with open('output_data.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Path','len of pg_no and subjects','Page nos',"subjects"])
        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file)
                split_pdf_and_rename(pdf_path)
                print(pdf_path)
                page_numbers,subjects = get_subjects(pdf_path)
                print(len(page_numbers),len(subjects))
                print(page_numbers)
                print(subjects)
                writer.writerow([pdf_path,str([len(page_numbers),len(subjects)]),str(page_numbers),str(subjects)])
                all_subjects.update(subjects)
    return list(all_subjects)

# get_subjects_from_folder(r'/Users/gokulakrishnan/Desktop/extra study/Subject_Extractor/uploads')
