import flet
import flet_core
from pyodide.code import run_js


class WebDownloadButton(flet.FilledButton):

  @classmethod
  def use_in(cls, page: flet_core.page):
    cls.page = page

  page: flet_core.page = None

  def __init__(
    self,
    text: str,
    media: str,
    get_filename,
    on_download
  ):
    self.on_download = on_download

    def choose_and_download(e):
      try:
        path = f"/{get_filename()}"
        on_download(path)
        js_code = f"""
        (function() {{
          let data = pyodide.FS.readFile('{path}', {{ encoding: 'binary' }});
          let blob = new Blob([data], {{type: '{media}'}});
          let url = URL.createObjectURL(blob);
          return url;      
        }})()
        """
        url = run_js(js_code)
        WebDownloadButton.page.launch_url(url)
      except Exception as ex:
        print(f"Error: {ex}")

    flet.FilledButton.__init__(
      self,
      text=text,
      icon=flet.icons.DOWNLOAD,
      on_click=choose_and_download
    )

