# tasmota-exporter

Prometheus Exporter for Tasmotaa power meters.

Polls all the tasmota devices listed in config.py on Prometheus scrape.

## Configuration File
```
export_port = 8226
export_address = '::'

tasmota_addresses = [
    "192.168.x.x",
    "192.168.x.x",
    ]

```
#### tasmota_addresses
tasmota_addresses is a list of ip addresses of the tasmota devices.

## Installation
```
> podman pull quay.io/mjkantti/tasmota-exporter
```
```
> podman run --rm -it -p 8226:8226 -v {path_to_config.py}:/tasmota-exporter/config.py quay.io/mjkantti/tasmota-exporter
```

## Metrics
```
> curl {ip_running_tasmota-exporter}
```

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 23414.0
python_gc_objects_collected_total{generation="1"} 2273.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 83.0
python_gc_collections_total{generation="1"} 7.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="12",patchlevel="7",version="3.12.7"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.940352e+07
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 3.0089216e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.72811141719e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 128.54
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP tasmota_energy_total Tasmota Total Energy
# TYPE tasmota_energy_total counter
tasmota_energy_total{ip="192.168.x.x",mac="xx:xx:xx:xx:xx:xx"} 45.048 1728124027784
# HELP tasmota_current Tasmota Current
# TYPE tasmota_current gauge
tasmota_current{ip="192.168.21.191",mac="xx:xx:xx:xx:xx:xx"} 0.092 1728124027784
# HELP tasmota_voltage Tasmota Voltage
# TYPE tasmota_voltage gauge
tasmota_voltage{ip="192.168.x.x",mac="xx:xx:xx:xx:xx:xx"} 104.0 1728124027784
# HELP tasmota_power Tasmota Power
# TYPE tasmota_power gauge
tasmota_power{ip="192.168.x.x",mac="xx:xx:xx:xx:xx:xx"} 4.0 1728124027784
# HELP tasmota_uptime_total Tasmota Uptime in seconds
# TYPE tasmota_uptime_total counter
tasmota_uptime_total{ip="192.168.x.x",mac="xx:xx:xx:xx:xx:xx"} 9.597418e+06 1728124027784
```
