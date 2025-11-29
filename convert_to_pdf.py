#!/usr/bin/env python3
"""
Convert BUILD_GUIDE.md to PDF using reportlab
"""

import re
import os

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import HexColor
except ImportError:
    print("Installing required packages...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import HexColor

def parse_markdown_to_elements(md_content):
    """Parse markdown content and convert to reportlab elements"""
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#051334'),
        spaceAfter=15,
        spaceBefore=30,
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#051334'),
        spaceAfter=12,
        spaceBefore=25,
        borderWidth=1,
        borderColor=HexColor('#051334'),
        borderPadding=5,
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#051334'),
        spaceAfter=10,
        spaceBefore=20,
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=HexColor('#051334'),
        spaceAfter=8,
        spaceBefore=15,
    )
    
    h4_style = ParagraphStyle(
        'CustomH4',
        parent=styles['Heading4'],
        fontSize=12,
        textColor=HexColor('#051334'),
        spaceAfter=6,
        spaceBefore=12,
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        backColor=HexColor('#f4f4f4'),
        borderColor=HexColor('#051334'),
        borderWidth=1,
        borderPadding=10,
        leading=12,
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
    )
    
    # Split into lines
    lines = md_content.split('\n')
    in_code_block = False
    code_block_lines = []
    in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_block_lines)
                elements.append(Preformatted(code_text, code_style))
                code_block_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue
        
        # Handle headers
        if line.startswith('# '):
            text = line[2:].strip()
            elements.append(Paragraph(text, h1_style))
            elements.append(Spacer(1, 0.2*inch))
        elif line.startswith('## '):
            text = line[3:].strip()
            elements.append(Paragraph(text, h2_style))
            elements.append(Spacer(1, 0.15*inch))
        elif line.startswith('### '):
            text = line[4:].strip()
            elements.append(Paragraph(text, h3_style))
            elements.append(Spacer(1, 0.1*inch))
        elif line.startswith('#### '):
            text = line[5:].strip()
            elements.append(Paragraph(text, h4_style))
            elements.append(Spacer(1, 0.08*inch))
        elif line.strip() == '---':
            elements.append(Spacer(1, 0.3*inch))
        elif re.match(r'^[-*]\s+', line.strip()):
            # List item
            text = re.sub(r'^[-*]\s+', '', line.strip())
            # Escape HTML and format
            text = escape_html(text)
            # Handle inline formatting
            text = format_inline_markdown(text)
            elements.append(Paragraph(f"• {text}", normal_style))
        elif re.match(r'^\d+\.\s+', line.strip()):
            # Numbered list
            text = re.sub(r'^\d+\.\s+', '', line.strip())
            text = escape_html(text)
            # Handle inline formatting
            text = format_inline_markdown(text)
            elements.append(Paragraph(f"• {text}", normal_style))
        elif line.strip() == '':
            # Empty line
            if not in_list:
                elements.append(Spacer(1, 0.1*inch))
        else:
            # Regular paragraph
            text = line.strip()
            if text:
                text = escape_html(text)
                # Handle inline formatting
                text = format_inline_markdown(text)
                elements.append(Paragraph(text, normal_style))
        
        i += 1
    
    return elements

def escape_html(text):
    """Escape HTML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def format_inline_markdown(text):
    """Format inline markdown elements"""
    # Handle inline code (backticks)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9" color="#d63384">\1</font>', text)
    # Handle bold (**text**)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # Handle italic (*text*)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    return text

def markdown_to_pdf(markdown_file, pdf_file):
    """Convert markdown file to PDF"""
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Parse markdown and create elements
    elements = parse_markdown_to_elements(md_content)
    
    # Build PDF
    doc.build(elements)
    print(f"Successfully created PDF: {pdf_file}")

if __name__ == '__main__':
    markdown_to_pdf('BUILD_GUIDE.md', 'BUILD_GUIDE.pdf')
