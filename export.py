#!/usr/bin/python3
# -*- coding: utf-8 -*-

# importing the requests library
import requests
import sys
import logging

from signal import signal, SIGTERM, SIGINT
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from time import time, sleep

from config import export_port, export_address, tasmota_addresses

class TasmotaCollector(object):
    def __init__(self):
        self.metrics = {}

        self.headers = {"content-type": "application/json"}


    def collect(self):
        logging.debug("Incoming Request")

        self.get_metrics()

        labels = ['mac', 'ip']

        energy = CounterMetricFamily('tasmota_energy', 'Tasmota Total Energy', labels=labels)
        current = GaugeMetricFamily('tasmota_current', 'Tasmota Current', labels=labels)
        voltage = GaugeMetricFamily('tasmota_voltage', 'Tasmota Voltage', labels=labels)
        power = GaugeMetricFamily('tasmota_power', 'Tasmota Power', labels=labels)
        apparent_power = GaugeMetricFamily('tasmota_apparent_power', 'Tasmota Apparent Power', labels=labels)
        reactive_power = GaugeMetricFamily('tasmota_reactive_power', 'Tasmota Reactive Power', labels=labels)
        
        uptime = CounterMetricFamily('tasmota_uptime', 'Tasmota Uptime in seconds', labels=labels)

        for mac, data in self.metrics.items():
            label_values = [mac, data.get('StatusNET', {}).get('IPAddress')]

            pwr_metrics = data.get('StatusSNS', {}).get('ENERGY')
            ts = data.get('ts')
            if pwr_metrics:
                energy.add_metric(label_values, pwr_metrics['Total'], timestamp = ts)
                current.add_metric(label_values, pwr_metrics['Current'], timestamp = ts)
                voltage.add_metric(label_values, pwr_metrics['Voltage'], timestamp = ts)
                power.add_metric(label_values, pwr_metrics['Power'], timestamp = ts)
                apparent_power.add_metric(label_values, pwr_metrics['ApparentPower'], timestamp = ts)
                reactive_power.add_metric(label_values, pwr_metrics['ReactivePower'], timestamp = ts)

            info_metrics = data.get('StatusSTS')
            if info_metrics:
                uptime.add_metric(label_values, info_metrics.get('UptimeSec', 0), timestamp = ts)
            
        yield energy
        yield current
        yield voltage
        yield power
        yield uptime

    def get_metrics(self):
        logging.debug('...Fetching Data...')
        self.metrics = {}
        for addr in tasmota_addresses:
            try:
                cmd_url = f'http://{addr}/cm'
                x = requests.get(url = cmd_url, headers = self.headers, params = {'cmnd': 'status0'}, timeout=1)
    
                if not x.ok:
                    logging.warning(f'Could not get device Information: {x.reason}')
                    return
    
                data = x.json()
                data['ts'] = time()
                mac = data.get('StatusNET', {}).get('Mac')
                
                self.metrics[mac] = data

            except Exception as e:
                logging.warning(f'Got exception: {e}')

def exit_gracefully(signal, _):
    logging.warning(f"Caught signal {signal}, stopping")
    if server:
        server.shutdown()

    if thr:
        thr.join(5)
    
    sys.exit(1)


if __name__ == "__main__":
    signal(SIGINT, exit_gracefully)
    signal(SIGTERM, exit_gracefully)
        
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    collector = TasmotaCollector()
    REGISTRY.register(collector)

    global server, thr
    server, thr = start_http_server(export_port, export_address)

    while True:
        sleep(600)
