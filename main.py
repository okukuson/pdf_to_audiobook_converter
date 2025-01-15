from pypdf import PdfReader


class Pdf_to_AudioBook:
    def __init__(self,pdf_file):
        self.pdf = pdf_file
        self.extracted_text = None

    # Function to extract the text in the pdf file
    def text_extractor(self):
        out_put = []
        reader = PdfReader(self.pdf)
        for numb in range(len(reader.pages)):
            page = reader.pages[numb]
            text = page.extract_text()
            out_put.append(text)
        # print(out_put)
        self.extracted_text = out_put

    # Convert the text file into audio
    def text_to_audio(self):
        pass




pdf_file = 'file.pdf'

if __name__ == '__main__':
    converter = Pdf_to_AudioBook(pdf_file)
    converter.text_extractor()