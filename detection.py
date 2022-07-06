import cv2
import numpy as np
import plotly.express as px
from collections import defaultdict
from os import listdir, walk
from os.path import isfile, join
from typing import NamedTuple
from imutils.object_detection import non_max_suppression
from pprint import pprint

class TemplateMatch(NamedTuple):
	match_type: str
	name: str
	precision: float
	x: int
	y: int

class Detector:
	def __init__(self):
		self.load_assets()

	def load_assets(self):
		w = walk('assets/templates')
		_, directories, _ = next(w)
		self._templates = defaultdict(list)

		for directory in directories:
			root, _, files = next(w)
			for file in files:
				img = cv2.imread(join(root, file))
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				self._templates[directory].append({
					'name': file.partition('.')[0],
					'image': img
				})


	def find_all(self, image, match=None):
		if not match:
			match = self._templates.keys()
		
		matches = []
		clone = image.copy()

		for match_type in [key for key in self._templates.keys() if key in match]:
			for template in self._templates[match_type]:
				(tH, tW) = template['image'].shape[:2]
				result = cv2.matchTemplate(image, template['image'], cv2.TM_CCOEFF_NORMED)
				(y_coords, x_coords) = np.where(result >= 0.75)

				rects = []
				for (x, y) in zip(x_coords, y_coords):
					rects.append((x, y, x + tW, y + tH))

				pick = non_max_suppression(np.array(rects))
				for (startX, startY, endX, endY) in pick:
					#cv2.rectangle(clone, (startX-48, startY-50), (endX+135, endY+120), (255, 0, 0), 2)
					cv2.rectangle(clone, (startX, startY+13), (endX+72, endY+90), (255, 0, 0), 2)
					matches.append(TemplateMatch(match_type, template['name'], result[startY][startX], startX, startY))
			
		return clone, matches


if __name__ == '__main__':
	image = cv2.imread('screenshots\\1657060180.3043032.png')
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	detector = Detector()
	img, matches = detector.find_all(image, match=['ux'])
	pprint(matches)
	px.imshow(img).show()
	