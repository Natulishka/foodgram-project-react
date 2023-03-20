from datetime import datetime

from django.conf import settings
from fpdf import FPDF


class CustomPDF(FPDF):

    def header(self):
        self.set_font('Arial', size=8)
        self.cell(0, 10, 'Created by Foodgtam', ln=1)
        self.cell(0, 10, 'Author: Shulgina Natalya', ln=1)
        self.cell(0, 10, datetime.now().strftime("%d.%m.%Y %H:%M"), ln=1)
        self.ln(20)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        page = 'Page ' + str(self.page_no())
        self.cell(0, 10, page, 0, 0, 'C')


def make_file(file, ext, ingredients):
    if ext == '.txt':
        with open(file + ext, 'w', encoding='utf-8') as f:
            f.write('Choping cart:' + '\n')
            f.write('\n')
            counter = 1
            for ingredient in ingredients:
                text = (f"{counter}. "
                        f"{ingredient['ingredient__name'].capitalize()} "
                        f"({ingredient['ingredient__measurement_unit__name']})"
                        f" - {ingredient['amount']} \n")
                f.write(text)
                counter += 1
            f.write('\n')
            f.write('\n')
            f.write('Created by Foodgtam' + '\n')
            f.write('Author: Shulgina Natalya' + '\n')
            f.write(datetime.now().strftime("%d.%m.%Y %H:%M"))
    elif ext == '.pdf':
        pdf = CustomPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', settings.MEDIA_ROOT +
                     '/fonts/DejaVuSansCondensed.ttf',
                     uni=True)
        pdf.set_font('DejaVu', size=18)
        pdf.cell(0, 10, txt='Choping cart:', ln=1)
        pdf.cell(0, 10, txt='', ln=1)
        pdf.cell(0, 10, txt='', ln=1)
        counter = 1
        pdf.set_font_size(12)
        for ingredient in ingredients:
            text = (f"{counter}. "
                    f"{ingredient['ingredient__name'].capitalize()} "
                    f"({ingredient['ingredient__measurement_unit__name']})"
                    f" - {ingredient['amount']}")
            pdf.cell(0, 10, txt=text, ln=1)
            counter += 1
        pdf.output(file + ext)
