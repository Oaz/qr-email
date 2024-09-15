import flet_core
import platform

isWeb = platform.system() == 'Emscripten'
if isWeb:
  from WebDownloadButton import WebDownloadButton
else:
  from NativeDownloadButton import NativeDownloadButton


class DownloadButton:

  @classmethod
  def use_in(cls, page: flet_core.page):
    if isWeb:
      WebDownloadButton.use_in(page)
    else:
      NativeDownloadButton.use_in(page)

  @classmethod
  def create(cls, text: str, media: str, get_filename, on_download):
    if isWeb:
      return WebDownloadButton(text, media, get_filename, on_download)
    else:
      return NativeDownloadButton(text, get_filename, on_download)
