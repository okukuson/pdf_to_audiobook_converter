from pypdf import PdfReader
from gtts import gTTS
import os
from pathlib import Path


class Pdf_to_AudioBook:
    def __init__(self, pdf_file, lan='en', speed=False):
        self.pdf = pdf_file
        self.extracted_text = None
        self.lang = lan
        self.speed = speed

    # Function to extract the text in the pdf file
    def text_extractor(self):
        print(f'\nText is being extracted from {self.pdf}')
        out_put = []
        reader = PdfReader(self.pdf)
        for numb in range(len(reader.pages)):
            page = reader.pages[numb]
            text = page.extract_text()
            out_put.append(text)
        # print(out_put)
        self.extracted_text = "\n".join(out_put)
        print('\nText extraction Successful!!!')

    # Convert the text file into audio
    def text_to_audio(self,):
        print('\nText is being converted to audio, please wait...')
        audio = gTTS(text=self.extracted_text, lang=self.lang, slow=self.speed)
        output = os.path.split(pdf)[1]
        output = output.split('.')[0]
        output_file = f'{output}.mp3'
        audio.save(output_file)
        print('\npdf has been successfully converted to audio and saved in same directory as the script')

    # Run the process of pdf to audiobook conversion
    def run(self):
        self.text_extractor()
        self.text_to_audio()



if __name__ == '__main__':
    print('PDF to Audiobook')
    pdf = Path(input('Enter path to the pdf file: '))
    if pdf.is_file() and pdf.suffix == '.pdf':
        print(f'\n{pdf} has been successfully loaded')
        converter = Pdf_to_AudioBook(pdf)
        converter.run()
    else:
        print("File doesn't exist, please try again and enter a valid PDF file")

