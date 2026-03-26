from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import rl_config
import os

# Enable shaping
rl_config.allow_shaping = True

def test_tamil_pdf():
    # font_path = "c:\\Users\\Lithi\\OneDrive\\Desktop\\AgriNova-final\\AgriNova-app\\backend\\NotoSansTamil-Regular.ttf"
    font_path = os.path.join(os.getcwd(), "NotoSansTamil-Regular.ttf")
    if not os.path.exists(font_path):
        print(f"Font not found at {font_path}")
        return

    pdfmetrics.registerFont(TTFont("NotoSansTamil", font_path))
    
    styles = getSampleStyleSheet()
    tamil_style = ParagraphStyle(
        'TamilStyle',
        parent=styles['Normal'],
        fontName='NotoSansTamil',
        fontSize=12,
        leading=15
    )
    
    doc = SimpleDocTemplate("tamil_test.pdf", pagesize=A4)
    story = []
    
    # "விவசாயி" (Farmer)
    text = "விவசாயி பெயர்: ரகு"
    story.append(Paragraph(text, tamil_style))
    
    doc.build(story)
    print("PDF generated as tamil_test.pdf")

if __name__ == "__main__":
    test_tamil_pdf()
