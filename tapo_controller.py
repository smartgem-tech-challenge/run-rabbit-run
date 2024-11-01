from config import Config
from tapo import ApiClient
import colorsys
import logging

class TapoController
    def __init__(self):
        self.client = ApiClient(Config.TAPO_USERNAME, Config.TAPO_PASSWORD)
        self.initialized_bulbs = {}

    async def initialize_bulbs(self, bulbs):
        try:
            for bulb in bulbs:
                self.initialized_bulbs[bulb["id"]] = await self.client.l530(bulb["ip_address"])
                await self.control_bulb(bulb["id"], bulb["state"], bulb["brightness"], bulb["color"])
                
                logging.info(f"Initialized bulb {bulb["id"]} ({bulb["ip_address"]}).")
        except Exception as error:
            logging.error(error)

    async def get_bulb(self, id):
        not id in self.initialized_bulbs:
            raise ValueError(f"Invalid bulb: {id} - bulb not initialized.")
        
        return self.initialized_bulbs[id]

    async def control_bulb(self, id, state, brightness, color):
        try:
            bulb = await self.get_bulb(id)

            if state == "off":
                await bulb.off()
            else:
                hue, saturation = self.convert_hex_to_hue_saturation(color)

                await bulb.set_brightness(brightness)
                await bulb.set_hue_saturation(hue, saturation)

            logging.info(f"Controlled bulb {id} - state: {state}, brightness: {brightness}, color: {color}.")
        except Exception as error:
            logging.error(error)

    def convert_hex_to_hue_saturation(self, hex_color):
        hex_color = hex_color.lstrip("#")

        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        hue = int(h * 360)
        saturation = int(s * 100)

        if saturation == 0:
            saturation = 1

        return hue, saturation