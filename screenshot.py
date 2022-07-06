from PIL import ImageGrab
from time import sleep, time
from PIL.Image import Image
from win32gui import GetWindowText, EnumWindows, GetWindowRect, SetForegroundWindow
from pywintypes import error

class WindowNotFoundError(ValueError):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class Screenshot:
	def __init__(self, target: str, dpi: float=1.0) -> None:
		self._target = target
		self._dpi = dpi
		self._hwnd = None

	def _get_window_handle(self) -> int:
		toplist, winlist = [], []
		EnumWindows(lambda hwnd, _: winlist.append((hwnd, GetWindowText(hwnd))), toplist)

		windows = [(hwnd, title) for hwnd, title in winlist if self._target in title.lower()]
		
		if not windows:
			raise WindowNotFoundError(f'No window with name "{self._target}" found')
		
		return windows[0][0]

	def take_screenshot(self, save: bool=True) -> Image:
		if not self._hwnd:
			self._hwnd = self._get_window_handle()

		# SetForegroundWindow(self._hwnd)
		try:
			bbox = GetWindowRect(self._hwnd)
		except error:
			self._hwnd = self._get_window_handle()
			bbox = GetWindowRect(self._hwnd)
		
		bbox = tuple([n*self._dpi for n in bbox])
		img = ImageGrab.grab(bbox, all_screens=True)

		if save:
			img.save(f'screenshots/{time()}.png')	

		return img


if __name__ == '__main__':
	screenshot = Screenshot(target='league of legends', dpi=1.25)
	while True:
		try:
			screenshot.take_screenshot()
			sleep(10)
		except WindowNotFoundError as e:
			print(e)
			input('Press enter key to continue...')