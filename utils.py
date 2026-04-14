from fpdf import FPDF
import os

def generate_receipt(order_id, timestamp, staff_name, items, total_amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Cafe Management System", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Official Receipt", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Order ID: {order_id}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Date: {timestamp}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Served By: {staff_name}", ln=True, align='L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Items
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(80, 10, "Item", 0, 0)
    pdf.cell(40, 10, "Quantity", 0, 0)
    pdf.cell(40, 10, "Price", 0, 0)
    pdf.cell(30, 10, "Total", 0, 1)
    
    pdf.set_font("Arial", size=10)
    for item in items:
        pdf.cell(80, 10, item['name'], 0, 0)
        pdf.cell(40, 10, str(item['quantity']), 0, 0)
        pdf.cell(40, 10, f"Rs. {item['price']:.2f}", 0, 0)
        pdf.cell(30, 10, f"Rs. {(item['quantity'] * item['price']):.2f}", 0, 1)
        
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Total
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(160, 10, "Total Amount:", 0, 0, 'R')
    pdf.cell(30, 10, f"Rs. {total_amount:.2f}", 0, 1)
    
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Thank you for your visit!", ln=True, align='C')
    
    # Save PDF
    receipts_dir = os.path.join(os.path.dirname(__file__), "receipts")
    if not os.path.exists(receipts_dir):
        os.makedirs(receipts_dir)
        
    filename = f"receipt_{order_id}.pdf"
    file_path = os.path.join(receipts_dir, filename)
    pdf.output(file_path)
    return filename
