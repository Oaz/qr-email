import urllib
from datetime import datetime
import flet as ft
import pyqrcode
from flet_core import ScrollMode

from DownloadButton import DownloadButton


def main(page: ft.Page):
  site_url = "https://qr-email.mnt.space/"
  page.title = "QR-Email"
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.window.min_height = 1000
  page.window.min_width = 600
  page.scroll = ScrollMode.HIDDEN

  qr_image = ft.Ref[ft.Image]()
  qr_email = ft.Ref[ft.TextField]()
  qr_topic = ft.Ref[ft.TextField]()
  qr_body = ft.Ref[ft.TextField]()

  def encode(f):
    if f.current.value.strip():
      return urllib.parse.quote_plus(f.current.value)
    else:
      return ""

  def generate_qrcode():
    info = "\n\n" + site_url
    qr_text = f"mailto:{encode(qr_email)}?subject={encode(qr_topic)}&body={encode(qr_body) + info}"
    return pyqrcode.create(qr_text)

  def update_qrcode(e):
    qr_code = generate_qrcode()
    qr_image.current.src_base64 = qr_code.png_as_base64_str(scale=20)
    qr_image.current.update()

  def download_as_svg(qr_code, path):
    qr_code.svg(path, scale=20)

  def download_as_png(qr_code, path):
    qr_code.png(path, scale=20)

  # def download_as_pdf(qr_code, path):
  #   buffer = io.BytesIO()
  #   qr_code.png(buffer, scale=20)
  #   pdf_bytes = img2pdf.convert(buffer.getvalue())
  #   with open(path, "wb") as pdf_file:
  #     pdf_file.write(pdf_bytes)

  def define_filename(extension):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"QR code {qr_topic.current.value} {now}.{extension}"

  def create_download_button(text, media, extension, download):
    return DownloadButton.create(
      text=text,
      media=media,
      get_filename=lambda: define_filename(extension),
      on_download=lambda path: download(generate_qrcode(), path) if path is not None else None,
    )

  DownloadButton.use_in(page)
  page.add(
    ft.Column(
      controls=[
        ft.TextField(
          ref=qr_email,
          label="Adresse email du destinataire",
          keyboard_type=ft.KeyboardType.EMAIL,
          on_change=update_qrcode,
          autofocus=True
        ),
        ft.TextField(
          ref=qr_topic,
          label="Objet de l'email",
          on_change=update_qrcode,
          autofocus=True
        ),
        ft.TextField(
          ref=qr_body,
          label="Corps du message",
          multiline=True,
          min_lines=5,
          max_lines=5,
          on_change=update_qrcode,
          autofocus=True
        ),
      ]
    ),
    ft.Divider(),
    ft.Container(
      ft.Image(
        ref=qr_image,
        width=600,
        height=600,
      ),
      alignment=ft.alignment.center
    ),
    ft.Row(
      controls=[
        create_download_button("SVG", "image/svg+xml", "svg", download_as_svg),
        create_download_button("PNG", "image/png", "png", download_as_png),
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    ),
  )
  update_qrcode(None)


if __name__ == "__main__":
  ft.app(target=main, assets_dir="assets")
