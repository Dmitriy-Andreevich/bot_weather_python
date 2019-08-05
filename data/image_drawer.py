from datetime import datetime
from io import BytesIO
from urllib.request import urlopen

from PIL import ImageDraw, Image

from data.properties import *
from data.util import get_icon_link, get_modify_temp

TEMP_IMG_NAME = 'background.png'


def create_weather_image(req):
    file = BytesIO()
    background = Image.open('%s' % BACKGROUND_IMAGE).convert('RGBA')
    background.thumbnail((BG_WIDTH, BG_HEIGHT), Image.ANTIALIAS)
    paint_layer = ImageDraw.Draw(background)

    temps = []

    first_item_value = next(iter(req))

    bottom_element_start_x_coord_local = BOTTOM_ELEMENT_START_X_COORD

    draw_bottom_area(background, bottom_element_start_x_coord_local, paint_layer, req, temps)

    draw_top_area(background, first_item_value, paint_layer, temps)

    background.save(file, 'png')
    file.name = '%s' % TEMP_IMG_NAME
    file.seek(0)
    return file


def draw_top_area(background, first_item_value, paint_layer, temps):
    cl = Image.open(urlopen(get_icon_link(first_item_value[0]['weather'][0]["icon"]))).convert("RGBA")
    background.paste(cl, TOP_WEATHER_ICO_COORD, cl)
    paint_layer.text((TOP_ELEMENT_TEMP_X_COORD, TOP_ELEMENT_TEMP_Y_COORD),
                     get_modify_temp(int(first_item_value[0]['main']['temp'])) + "°C",
                     fill=(255, 255, 255), font=TOP_TEMP_FONT)
    paint_layer.text((TOP_ELEMENT_DESC_X_COORD, TOP_ELEMENT_DESC_Y_COORD),
                     str(first_item_value[0]['weather'][0]['description']),
                     fill=(255, 255, 255), font=TOP_DESC_FONT)
    paint_layer.text((TOP_ELEMENT_DESC_X_COORD, TOP_ELEMENT_DESC_Y_COORD + MIN_TEMP_Y_OFFSET),
                     "Минимальная температура: " + str(min(temps)) + "°C",
                     fill=(255, 255, 255), font=BOTTOM_TIME_FONT)
    paint_layer.text((TOP_ELEMENT_DESC_X_COORD, TOP_ELEMENT_DESC_Y_COORD + MAX_TEMP_Y_OFFSET),
                     "Максимальная температура: " + str(max(temps)) + "°C",
                     fill=(255, 255, 255), font=BOTTOM_TIME_FONT)
    paint_layer.text((TOP_ELEMENT_DESC_X_COORD, TOP_ELEMENT_DESC_Y_COORD + BAR_Y_OFFSET),
                     "Давление: " + str(int(first_item_value[0]['main']['pressure'])) + " bar",
                     fill=(255, 255, 255), font=BOTTOM_TIME_FONT)
    paint_layer.text((TOP_ELEMENT_DESC_X_COORD, TOP_ELEMENT_DESC_Y_COORD + WIND_Y_OFFSET),
                     "Скорость ветра: " + str(int(first_item_value[0]['wind']['speed'])) + " м/с",
                     fill=(255, 255, 255), font=BOTTOM_TIME_FONT)


def draw_bottom_area(background, bottom_element_start_x_coord_local, paint_layer, req, temps):
    for day in req:
        for el in day:
            temps.append(int(el['main']['temp']))
            if req.__len__() > 1 and datetime.fromtimestamp(el['dt']).hour != 12:
                continue
            else:
                paint_layer.text((bottom_element_start_x_coord_local + BOTTOM_ELEMENT_TEMP_OFFSET_X_CORD,
                                  BOTTOM_ELEMENT_START_Y_COORD + BOTTOM_ELEMENT_FIRST_LINE_OFFSET_Y_CORD),
                                 get_modify_temp(int(el['main']['temp'])),
                                 fill=(255, 255, 255), font=BOTTOM_TEMP_FONT)
                cl = Image.open(urlopen(get_icon_link(el['weather'][0]["icon"]))).convert("RGBA")
                background.paste(cl, (
                    bottom_element_start_x_coord_local,
                    BOTTOM_ELEMENT_START_Y_COORD + BOTTOM_ELEMENT_SECOND_LINE_OFFSET_Y_CORD),
                                 cl)
                paint_layer.text((bottom_element_start_x_coord_local + BOTTOM_ELEMENT_DATETIME_OFFSET_X_CORD,
                                  BOTTOM_ELEMENT_START_Y_COORD + BOTTOM_ELEMENT_THIRD_LINE_OFFSET_Y_CORD),
                                 datetime.fromtimestamp(el['dt']).strftime('%H:%M'), fill=(255, 255, 255),
                                 font=BOTTOM_TIME_FONT)
                paint_layer.text((bottom_element_start_x_coord_local + BOTTOM_ELEMENT_DATETIME_OFFSET_X_CORD,
                                  BOTTOM_ELEMENT_START_Y_COORD + BOTTOM_ELEMENT_THIRD_LINE_OFFSET_Y_CORD + 25),
                                 datetime.fromtimestamp(el['dt']).strftime('%d.%m'), fill=(255, 255, 255),
                                 font=BOTTOM_TIME_FONT)
                bottom_element_start_x_coord_local += BOTTOM_ELEMENT_OFFSET_X_CORD
