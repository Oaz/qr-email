import flet
import flet_core


class NativeDownloadButton(flet.FilledButton):

  @classmethod
  def use_in(cls, page: flet_core.page):
    page.overlay.append(cls.file_picker)

  @classmethod
  def download(cls, e):
    cls.selected_button.on_download(e.path)

  selected_button = None
  file_picker = flet.FilePicker(
    on_result=lambda e: NativeDownloadButton.download(e)
  )

  def __init__(
    self,
    text: str,
    get_filename,
    on_download,
  ):
    self.on_download = on_download

    def choose_and_download(e):
      NativeDownloadButton.selected_button = self
      fn = get_filename()
      NativeDownloadButton.file_picker.save_file(
        dialog_title=text,
        file_name=fn,
      )

    flet.FilledButton.__init__(
      self,
      text=text,
      icon=flet.icons.DOWNLOAD,
      on_click=choose_and_download
    )
