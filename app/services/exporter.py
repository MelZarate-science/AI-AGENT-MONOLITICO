from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


# Cargar plantillas desde /app/templates
env = Environment(loader=FileSystemLoader("app/templates"))


def export_to_html(narrative: str) -> str:
    """
    Renderiza un HTML válido usando Jinja2.
    """
    template = env.get_template("narrative.html")
    return template.render(narrative=narrative)


def export_to_pdf(narrative: str) -> bytes:
    """
    Convierte el HTML a PDF utilizando WeasyPrint.
    """
    html_str = export_to_html(narrative)
    pdf_bytes = HTML(string=html_str).write_pdf()
    return pdf_bytes