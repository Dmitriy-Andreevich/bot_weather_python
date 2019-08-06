#
from PIL import ImageFont

### BOT START
BOT_TOKEN = '817721430:AAE_P9ytcgz3skzPV7jqiZceB8yy-O2Bgpk'
### BOT START

### WEATHER API START
WEATHER_API_KEY = "7d591840fba74434fc81156186ec42c3"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
WEATHER_IMAGE_URL = "http://openweathermap.org/img/wn/"
### WEATHER API START

### DRAW IMAGE START
BG_HEIGHT = 1035
BG_WIDTH = 690

TOP_ELEMENT_START_X_COORD = 40
TOP_ELEMENT_START_Y_COORD = 150

TOP_ELEMENT_TEMP_X_COORD = TOP_ELEMENT_START_X_COORD
TOP_ELEMENT_TEMP_Y_COORD = TOP_ELEMENT_START_Y_COORD

TOP_ELEMENT_CITY_X_COORD = TOP_ELEMENT_START_X_COORD
TOP_ELEMENT_CITY_Y_COORD = 320

TOP_ELEMENT_DESC_X_COORD = TOP_ELEMENT_START_X_COORD
TOP_ELEMENT_DESC_Y_COORD = 390

BACKGROUND_IMAGE = 'img/bg.jpg'
TOP_WEATHER_ICO_COORD = (300, 50)
WIND_Y_OFFSET = 160
BAR_Y_OFFSET = 130
MAX_TEMP_Y_OFFSET = 100
MIN_TEMP_Y_OFFSET = 70

BOTTOM_ELEMENT_START_X_COORD = 20
BOTTOM_ELEMENT_START_Y_COORD = BG_HEIGHT - 250
BOTTOM_ELEMENT_OFFSET_X_CORD = 80
BOTTOM_ELEMENT_TEMP_OFFSET_X_CORD = 30
BOTTOM_ELEMENT_DATETIME_OFFSET_X_CORD = 20

BOTTOM_ELEMENT_FIRST_LINE_OFFSET_Y_CORD = 0
BOTTOM_ELEMENT_SECOND_LINE_OFFSET_Y_CORD = 40
BOTTOM_ELEMENT_THIRD_LINE_OFFSET_Y_CORD = 130

DEF_FONT = "font/17601.ttf"
TOP_TEMP_FONT = ImageFont.truetype(DEF_FONT, 170)
TOP_CITY_FONT = ImageFont.truetype(DEF_FONT, 50)
TOP_DESC_FONT = ImageFont.truetype(DEF_FONT, 60)
BOTTOM_TIME_FONT = ImageFont.truetype(DEF_FONT, 24)
BOTTOM_TEMP_FONT = ImageFont.truetype(DEF_FONT, 32)
### DRAW IMAGE END

### BUTTONS START
WEATHER_TODAY_BUTTON_TEXT = "Погода на сутки"
WEATHER_5_DAY_BUTTON_TEXT = "Погода на 6 дней"
HELP_BUTTON_TEXT = "Помощь"
PROFILE_BUTTON_TEXT = "Мой профиль"
WEATHER_SUBSCRIBE_BUTTON_TEXT = "Функция \"погода утром\""

CHANGE_LOCATION_TEXT = "Для смены домашней локации просто отправьте боту новое местоположение, после чего выберите соответствующий пункт меню."
SUBSCRIBE_CALL_TEXT = "Подпишись и получай свежую и актуальную информацию в твоем регионе!"
HELP_TEXT = "Информация об основных функциях бота"


TEXT_COMMAND_NOT_FOUND = "Наверное вы ошиблись"
ERROR_HOME_LOCATION_MESSAGE = "Добавьте домашнюю локацию. Просто отправьте свою локацию боту. И выберите соответствующий пункт"

REGION_WEATHER_ON_DAY_TEXT = "Погода в регионе на сутки"
REGION_WEATHER_ON_WEAK_TEXT = "Погода на 6 дней"
SET_HOME_LOCATION_TEXT = "Установить домашнюю локацию"
REFRESH_HOME_LOCATION_TEXT = "Обновить домашнюю локацию"
HOME_LOCATION_REFRESH_SUCCESS = "Домашняя локация обновлена"
SELECT_ACTION_TEXT = "Выберите действие."
SUBSCRIPTION_ON = "Вы подписались на рассылку"
SUBSCRIPTION_OFF = "Вы отписались от рассылки погоды"
### BUTTONS END
