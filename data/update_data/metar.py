from metar import Metar
import requests
import pytaf


class AviationWeather(object):
    METAR_URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT"
    TAF_URL = "http://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{}.TXT"

    def get_clean_response(self, response):
        clean_response = response.text.split('\n')
        clean_response = clean_response[1:-1]
        return clean_response

    def normalizate_taf(self, response):
        s = ""
        for i in response:
            s = s + " " + i.strip()
        s = s.strip()
        return s

    def decode_taf(self, s):
        taf = pytaf.TAF(s)
        decoder = pytaf.Decoder(taf)
        return decoder

    def get_metar(self, icao_code):
        session = requests.Session()
        response = session.get(self.METAR_URL.format(icao_code))
        response = self.get_clean_response(response)[0]

        obs = Metar.Metar(response)
        return obs

    def get_taf(self, icao_code):
        session = requests.Session()
        response = session.get(self.TAF_URL.format(icao_code))
        response = self.get_clean_response(response)

        response = self.normalizate_taf(response)
        obs = self.decode_taf(response)
        # summary = decoder.decode_taf().strip()
        return obs
