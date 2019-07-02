"""
Prometheus collecters for airfilter sensors.
"""
import time
from prometheus_client import CollectorRegistry, generate_latest, Info
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from sds011 import SDS011
from pwm import PWM
from ccs811.CCS811_RPi import CCS811_RPi
from ccs811.SDL_Pi_HDC1000 import *

class AirfilterCollector(object):
    """
    Collects airfilter information, i.e. dust concentration in pm 10 & 2,5
    usage for cluster nodes and guests.
    """

    def __init__(self, sds011, sleep, ccs811):
        self._sds011  = sds011
        self._sleep   = sleep
        self._ccs811  = ccs811

    def collect(self):
        sds011 = SDS011(self._sds011, use_query_mode=True)
        sds011.sleep(sleep=False)
        time.sleep(int(self._sleep))

        sds011s = tuple(sds011.query())

        sds011.sleep()

        pm25 = GaugeMetricFamily('airfilter_dust', 'dust of size 2,5', labels=['sensor', 'pm'])
        pm25.add_metric(['sds011', '2.5'], sds011s[0])
        yield pm25

        pm10 = GaugeMetricFamily('airfilter_dust', 'dust of size 10', labels=['sensor', 'pm'])
        pm10.add_metric(['sds011', '10'], sds011s[1])
        yield pm10

        if self._ccs811 == 'true':
            ccs811 = CCS811_RPi()

            configuration = 0b100000
            ccs811.configureSensor(configuration)

            hdc1000 = SDL_Pi_HDC1000()
            hdc1000.turnHeaterOff()
            hdc1000.setTemperatureResolution(HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
            hdc1000.setHumidityResolution(HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)

            humidity = hdc1000.readHumidity()
            temperature = hdc1000.readTemperature()

            ccs811.setCompensation(temperature,humidity)

            humid = GaugeMetricFamily('airfilter_humidity', 'humidity reading', labels=['sensor'])
            humid.add_metric(['ccs811'], humidity)
            yield humid

            temp = GaugeMetricFamily('airfilter_temperature', 'temperature reading', labels=['sensor'])
            temp.add_metric(['ccs811'], temperature)
            yield temp

            statusbyte = ccs811.readStatus()
            status = GaugeMetricFamily('airfilter_statusbyte', 'statusbyte', labels=['sensor', 'statusbyte'])
            status.add_metric(['ccs811', bin(statusbyte)], 1)
            yield status

            error = ccs811.checkError(statusbyte)

            failure = GaugeMetricFamily('airfilter_error', '1 if error on sensor', labels=['sensor'])
            if(error):
                failure.add_metric(['ccs811'], 1)
            else:
                failure.add_metric(['ccs811'], 0)
            yield failure

            samples = GaugeMetricFamily('airfilter_samples', '0 if no new samples', labels=['sensor'])
            res = GaugeMetricFamily('airfilter_result', '1 if valid result', labels=['sensor'])
            eco2 = GaugeMetricFamily('airfilter_eco2', 'eco2 reading', labels=['sensor', 'unit'])
            tvoc = GaugeMetricFamily('airfilter_tvoc', 'tvoc reading', labels=['sensor', 'unit'])

            if(ccs811.checkDataReady(statusbyte)):
                samples.add_metric(['ccs811'], 1)
                yield samples

                result = ccs811.readAlg();
                if(result):
                    res.add_metric(['ccs811'], 1)
                    yield res

                    eco2.add_metric(['ccs811', 'ppm'], result['eCO2'])
                    yield eco2

                    tvoc.add_metric(['ccs811', 'ppb'], result['TVOC'])
                    yield tvoc

                else:
                    res.add_metric(['ccs811'], 0)
                    yield res

                    eco2.add_metric(['ccs811', 'ppm'], 0)
                    yield eco2

                    tvoc.add_metric(['ccs811', 'ppb'], 0)
                    yield tvoc

            else:
                samples.add_metric(['ccs811'], 0)
                yield samples
                res.add_metric(['ccs811'], 0)
                yield res
                eco2.add_metric(['ccs811', 'ppm'], 0)
                yield eco2
                tvoc.add_metric(['ccs811', 'ppb'], 0)
                yield tvoc

def collect_sensors(sds011, sleep, ccs811):
    """Scrape sensors and return prometheus text format for it"""

    registry = CollectorRegistry()
    registry.register(AirfilterCollector(sds011, sleep, ccs811))
    return generate_latest(registry)
