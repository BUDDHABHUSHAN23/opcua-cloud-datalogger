# Report generation logic
import os
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from collections import defaultdict
from app.db.crud import tag as tag_crud, log as log_crud
from app.db.database import SessionLocal
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def generate_excel_report(schedule, start_dt, end_dt):
    db = SessionLocal()
    tags = tag_crud.get_tags_for_group(db, schedule.group_id)
    data_rows = log_crud.get_historical_data(db, schedule.group_id, start_dt, end_dt)
    db.close()

    if not data_rows:
        logging.info("No data found for Excel report.")
        return

    tag_names = [tag.alias or tag.node_id for tag in tags]
    pivoted = defaultdict(lambda: {name: "" for name in tag_names})
    for ts, alias, nodeid, value in data_rows:
        name = alias or nodeid
        pivoted[ts][name] = value

    save_path = os.path.join(schedule.output_folder, f"Report_{schedule.name}_{start_dt.strftime('%Y%m%d')}.xlsx")
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["Timestamp"] + tag_names)
    for ts, row in sorted(pivoted.items()):
        sheet.append([ts] + [row[name] for name in tag_names])
    wb.save(save_path)
    logging.info(f"Excel report saved: {save_path}")


def generate_pdf_report(schedule, start_dt, end_dt):
    db = SessionLocal()
    tags = tag_crud.get_tags_for_group(db, schedule.group_id)
    data_rows = log_crud.get_historical_data(db, schedule.group_id, start_dt, end_dt)
    db.close()

    if not data_rows:
        logging.info("No data found for PDF report.")
        return

    tag_names = [tag.alias or tag.node_id for tag in tags]
    pivoted = defaultdict(lambda: {name: "" for name in tag_names})
    for ts, alias, nodeid, value in data_rows:
        name = alias or nodeid
        pivoted[ts][name] = value

    save_path = os.path.join(schedule.output_folder, f"Report_{schedule.name}_{start_dt.strftime('%Y%m%d')}.pdf")
    doc = SimpleDocTemplate(save_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph(f"Report: {schedule.name}", styles['Title']), Spacer(1, 12)]

    data = [["Timestamp"] + tag_names]
    for ts, row in sorted(pivoted.items()):
        data.append([ts.strftime("%Y-%m-%d %H:%M:%S")] + [row[name] for name in tag_names])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    logging.info(f"PDF report saved: {save_path}")
