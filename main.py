from pypdf import PdfReader
from gtts import gTTS
import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename



class Pdf_to_AudioBook:
    def __init__(self, pdf_file, lan='en', speed=False):
        self.pdf = pdf_file
        self.extracted_text = None
        self.lang = lan
        self.speed = speed

    # Function to extract the text in the pdf file
    def text_extractor(self):
        # print(f'\nText is being extracted from {self.pdf}')
        out_put = []
        reader = PdfReader(self.pdf)
        for numb in range(len(reader.pages)):
            page = reader.pages[numb]
            text = page.extract_text()
            out_put.append(text)
        # print(out_put)
        self.extracted_text = "\n".join(out_put)
        # print('\nText extraction Successful!!!')

    # Convert the text file into audio
    def text_to_audio(self,):
        # print('\nText is being converted to audio, please wait...')
        audio = gTTS(text=self.extracted_text, lang=self.lang, slow=self.speed)
        output = os.path.split(self.pdf)[1]
        output = output.split('.')[0]
        output_file = os.path.join(app.config['UPLOAD_FOLDER'],f'{output}.mp3')
        audio.save(output_file)
        # print('\npdf has been successfully converted to audio and saved in same directory as the script')

    # Run the process of pdf to audiobook conversion
    def run(self):
        self.text_extractor()
        self.text_to_audio()

class UploadFile(FlaskForm):
    pdf_file = FileField(label='PDF file', validators=[DataRequired(), FileAllowed(['pdf'])])
    submit = SubmitField(label='Convert')


app = Flask(__name__)
app.secret_key = 'pdf_converter'
app.config['UPLOAD_FOLDER'] = 'upload'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def converter():
    form = UploadFile()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        file = form.data['pdf_file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('waiting', file=file_path))
    return render_template('interface.html', form=form)

@app.route('/converting/<file>')
def waiting(file):
    return render_template('working.html', file=file)

# @app.route('/success')
# def successful():
#     return render_template('successful.html')

@app.route('/processing/<file>')
def processing(file):
    pdfConverter = Pdf_to_AudioBook(file)
    pdfConverter.text_extractor()
    pdfConverter.text_to_audio()
    os.remove(file)
    return render_template('successful.html')


if __name__ == '__main__':
    app.run(debug=True)
    #
