from fpdf import FPDF

def general_pdf(nev, film, terem_szam, szekek, jegytipus):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="🎟️ Mozi Jegy", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Név: {nev}", ln=True)
    pdf.cell(200, 10, txt=f"Film: {film}", ln=True)
    pdf.cell(200, 10, txt=f"Terem: {terem_szam}", ln=True)
    pdf.cell(200, 10, txt=f"Szék(ek): {', '.join(map(str, szekek))}", ln=True)
    pdf.cell(200, 10, txt=f"Jegytípus: {jegytipus}", ln=True)

    pdf.output(f"jegy_{nev.replace(' ', '_')}.pdf")
