from io import StringIO
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTText, LTChar, LTAnno
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileReader
import os
import re
import argparse

def parse_title(layout):
    title = None
    up = None

    for textbox in layout:
        if not isinstance(textbox, LTText):
            continue
        for line in textbox:
            for char in line:
                if isinstance(char, LTAnno):
                    if char.get_text() != '\n':
                        title.append(char.get_text())
                elif isinstance(char, LTChar):
                    if title is None:
                        up = char.bbox[3]
                        title = []
                    # print(f'{char.get_text()} : {char.bbox[0]} {char.bbox[1]} {char.bbox[2]} {char.bbox[3]} {up}')
                    if char.bbox[3] == up:
                        title.append(char.get_text())
                    elif (up - char.bbox[3]) < 27.0:
                        up = char.bbox[3]
                        title.append(char.get_text())
                    else:
                        return ' '.join(''.join(title).split())

    if title is None:
        return None
    else:
        return ' '.join(''.join(title).split())


def guess_title(pdf_path):
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            return parse_title(layout)


def simple_get_title(pdf_path):
    pdf_reader = PdfFileReader(open(pdf_path, 'rb'), strict=False)
    pdf_title = pdf_reader.getDocumentInfo().title
    return pdf_title


def create_output_directory(output_path):
    duplicate_output_path = 0
    real_output_path = output_path

    while True:
        try:
            os.mkdir(real_output_path)
        except FileExistsError:
            real_output_path = output_path + str(duplicate_output_path)
            duplicate_output_path += 1
            continue
        output_path = real_output_path
        break

    return real_output_path


def convert_pdf_title(pdf_title):
    # remove special character in title
    pdf_title = re.sub('[^\w ]', '', pdf_title)
    # change all character to lower case
    pdf_title = str.lower(pdf_title)
    # substitute space with undercore
    pdf_title = re.sub(' ', '_', pdf_title)
    # rename pdf file and output as a new file
    return pdf_title


def get_title(pdf_path):
    pdf_title = simple_get_title(pdf_path)
    # print('get title failed')
    if pdf_title is None:
        pdf_title = guess_title(pdf_path)

    if pdf_title is None:
        return None
    else:
        return convert_pdf_title(pdf_title)


def copy_file(src_path, dst_path):
    if os.path.exists(dst_path):
        return False
    with open(src_path, 'rb') as src:
        with open(dst_path, 'wb') as dst:
            dst.write(src.read())
            return True

def convert_pdf(pdf_path, output_dir):
    pdf_title = get_title(pdf_path)
    if pdf_title is None:
        return

    output_pdf_path = os.path.join(output_dir, pdf_title + '.pdf')

    if copy_file(pdf_path, output_pdf_path):
        print(f'✅ {pdf_path} -> {output_pdf_path}')
    else:
        print(f'❌ {pdf_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract title from PDF.')
    parser.add_argument('--input', type=str, required=True,
                        help='PDF source directory or file.')
    parser.add_argument('--output_dir', type=str,
                        default='.', help='PDF Output directory.')
    args = parser.parse_args()

    if os.path.isfile(args.input):
        convert_pdf(args.input, args.output_dir)

    elif os.path.isdir(args.input):
        for root, dir_list, file_list in os.walk(args.input):
            for filename in file_list:
                convert_pdf(os.path.join(root, filename), args.output_dir)

        # os.path.exists(args.)
        # print(get_title('src/osdi/osdi22-reidys.pdf'))
        # print(get_title('src/osdi/osdi22-flinn.pdf'))
        # print(get_title('src/3411495.3421358.pdf'))
