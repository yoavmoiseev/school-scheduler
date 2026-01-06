from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


class PDFService:
    def export_schedule(self, schedule, config, title, output_path):
        """Export schedule to PDF using ReportLab"""
        
        weekdays = config.get('WEEKDAYS', 'Monday,Tuesday,Wednesday,Thursday,Friday').split(',')
        lessons_count = int(config.get('lessons', 8))
        lessons = list(range(1, lessons_count + 1))
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        # Build content
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_para = Paragraph(f'<b>{title}</b>', styles['Title'])
        elements.append(title_para)
        elements.append(Spacer(1, 0.5*cm))
        
        # Build table data
        table_data = []
        
        # Header row
        header = ['Lesson'] + [day.strip() for day in weekdays]
        table_data.append(header)
        
        # Data rows
        for lesson in lessons:
            row = [str(lesson)]
            for day in weekdays:
                day_trimmed = day.strip()
                lesson_data = schedule.get(day_trimmed, {}).get(lesson)
                if lesson_data:
                    cell_text = f"{lesson_data.get('subject', '')}\n{lesson_data.get('teacher', '')}"
                    if lesson_data.get('group'):
                        cell_text += f"\n({lesson_data.get('group')})"
                    row.append(cell_text)
                else:
                    row.append('')
            table_data.append(row)
        
        # Create table
        table = Table(table_data, repeatRows=1)
        
        # Style table
        table_style = TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # First column (lesson numbers)
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            
            # All cells
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])
        
        # Add colors to filled cells
        for row_idx, lesson in enumerate(lessons, start=1):
            for col_idx, day in enumerate(weekdays, start=1):
                day_trimmed = day.strip()
                lesson_data = schedule.get(day_trimmed, {}).get(lesson)
                if lesson_data and lesson_data.get('color_bg'):
                    try:
                        bg_color = colors.HexColor(lesson_data['color_bg'])
                        table_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), bg_color)
                    except:
                        pass
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        return output_path
