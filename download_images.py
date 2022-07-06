import requests
import re
from os import makedirs, path

#ui elements https://raw.communitydragon.org/latest/game/assets/ux/tft/


BASE_CHAMPIONS = 'https://raw.communitydragon.org/latest/game/assets/ux/tft/championsplashes/'
PATTERN_CHAMPIONS = r'<a href="(tft7.*?)"'
PATH_CHAMPIONS = './assets/store/'
makedirs(path.dirname(PATH_CHAMPIONS), exist_ok=True)


result = requests.get(BASE_CHAMPIONS).text
png = re.findall(PATTERN_CHAMPIONS, result)
png = [n for n in png if 'mobile' not in n]

for i in png:
	with open(f'{PATH_CHAMPIONS}{i}', 'wb') as f:
		f.write(requests.get(f'{BASE_CHAMPIONS}{i}', stream=True).content)



PATH_UX = './assets/ux/tfthealthbaratlas.png'
BASE_UX = 'https://raw.communitydragon.org/latest/game/assets/ux/tft/tfthealthbaratlas.png'
makedirs(path.dirname(PATH_UX), exist_ok=True)

with open(f'{PATH_UX}', 'wb') as f:
	f.write(requests.get(f'{BASE_UX}', stream=True).content)