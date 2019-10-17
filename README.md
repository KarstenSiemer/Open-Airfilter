# Open-Airfilter
Opensource air filtering system for your home

Since i have problems with pollen in the summer, i wanted to buy an air filtering system, but failed to find one that suits my needs.
Like being extremely silent or setting up schedules on when i want it to not run or that it should be even more silent when i want to go to sleep.

That is why i decided to just create my own and of course share my work.

Here are two pictures of it. (as an excuse, i am really not talented when it comes to working with wood)
![front view of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture1.jpg)
![insides of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture2.jpg)

This is how your grafana dashboard will look like:
![grafana screenshot dust graphs](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/grafana-airfilter.png)
Here you can see the most important graphs. One with the raw data that has been gathered by prometheus and the other where this
data is summed and averaged. This is done so that i have a singular point of orientation of how fast (or even at all) i want to spin the fans. Prometheus makes creating such data very easy. The query for this looks like this right now:

`sum(avg_over_time(airfilter_dust[10m]))`

Which just means to take a range vector of ten minutes of all instances of the metric `airfilter_dust`, of which there are two (pm 2,5 and 10) and calculate an average for each scrape point. Then sum the results together.

You could create queries that include data of more sensors and calculate the AQI (Air quality Index) for example and control your fans based on that. But i have found that to be unnecessary, since the only stuff i can filter is dust anyway.
You could however add an alertmanager to the docker-compose manifest and create prometheus alerts if some gas concentration is too high and send yourself an alert to open a window. 

If you also use the ccs811 sensor there are already dashboards prepared to monitor humidity, temperature, eco2 (equivalent calculated carbon-dioxide, within a range of 400 to 8192 parts per million (ppm)) and tvoc (Total Volatile Organic Compound) concentration within a range of 0 to 1187 parts per billion (ppb)).

## How to wire it up
The Raspberry Pi 3 b+ has four PWM pins but only two channels, so be aware when wiring the fans up.
I used pin 12 (PWM0) and pin 35 (PWM1).

If you have 5V fans you can directly connect them to the Pi's connectors.
I used pin 2 and pin 4.

Also connect them to ground pins.
I used pin 6 and pin 39.

The control wire of your PWM fans is not used right now. I want to implement monitoring using those connections in the exporter later on.

Either connect it directly or use a breadboard. If you want to connect more sensors, using the breadboard will benefit how tidy it looks and how much you can connect. Since with a breadboard you can share the power and ground pins.

Connect the sds011 by simply plugging it into USB. If you have more than one USB device connect, check to which ttyUSB it is connected. If it is not the default `/dev/ttyUSB0` then change the parameter for the sensor in the prometheus scrape targets.

## How to configure
The main configuration can be done in `/airfilter-manifest/docker-compose.yaml`
Here you can configure the fan controller in the service `airfilterfancontroller`

In `command` the second argument given to the python script is the query that the controller will use to get information from prometheus on how polluted the air is.

In the environment variables you can set:
* The [periods](https://en.wikipedia.org/wiki/Pulse-width_modulation) of your fans
* The time ranges for the modes
* The speed of your fans in six levels (this is relative to the period)
* Which amount of pollution maps to which level of fan speed

Also you can configure the targets of the prometheus in `/airfilter-manifest/prometheus/prometheus.yml`
Important here are the parameters with which prometheus is scraping the exporter, because they are actively configuring the airfilter-exporter.
There are three options here:
* sds011
  * where can the exporter find the sds011 sensor 
   (Default: '/dev/ttyUSB0')
* sleep
  * This controls how long the fan spins inside the sds011 sensor chamber before a measurement is made.
  * Generally you want a time that is long enough to exchange all the air in the chamber for accurate measurements (Default: 15 seconds)
* ccs811
  * This activates the optional ccs811 sensor

You can also change the retention time of the Prometheus. Either set it to a time range like 200h or configure retention based on the maximum size the timeseries database of prometheus is allowed to have like 25Gi. Or just set both like 1y and 25Gi, whatever happens first will be the chosen setting.

Because the airfilter-exporter is being configured by the URL with which it is scraped, you can query it with different parameters each scrape. Like connecting several sensors to the pi and configuring additional targets in prometheus where a different USB port is chosen in the params.
  
You could also build the containers yourself (Dockerfiles are included) and directly set the environment variables inside the containers, if you happen to not wanting to use docker-compose
  
#### Note the /boot/config.txt
Since we are be using PWM to drive the fans, we'll have to activate it in the boot config by appending this to the config:
`dtoverlay=pwm-2chan`

If you want to use the optional ccs811 chip, you'll have to active i²c also. To this, just append this:

`dtparam=i2c_arm=on`

## What i have used to build this:
* Raspberry pi 3 b+
  * This is overpowered for an airfilter, but i chose to put the whole stack on it, so it needs at least some beef
* Noctua NF-A14 5V PWM
  * I chose this because i do not have to change voltage to use it
  * You can use any fan of any size, just make sure that it can be used it PWM
  * I have used two fans because the filter is quite thick and with two air is being pushed and pulled. Which allows for more airflow through the filter 
* Nova PM Sensor SDS011 High Precision PM2.5
  * Most accurate sensor on consumer market (to my knowledge)
  * But it has the downside that it needs a fan to suck fresh air into it's chamber (sadly, i can hear it sometimes)
  * Also take some tubing to elongate the the rod where it sucks in air, so you can directly suck from the airflow of the fans
* 140mm fan grill
  * For the backside of the airfilter to fight of huge dust particles and protect the inside wiring
* HEPA-Filter
  * Mine is square (17 x 17 x 6 cm)
  * I'd recomment one with four stages of filtration (Pre-Filter, HEPA-Filter, Carbon-Filter, Sterilization-Cotton)
* Some eva feet to put the wooden box on
* A box to place the components in (i used wood)
  * This is more simple than it appears. By box is basically a canal with some standoffs infront and behind the filter. This fixates the filter and the fans and also places the fans directly into the middle of the filter, because they are a bit smaller than the filter
* Optional: CCS811 HDC1080 sensor
  * Nice way to get even more information about the air you breath in every day.
  * It gives information about temperature, humidity, co2 and tvoc
* Optional: Breadboard
  * I added in advance, just in case i want to add more sensors
* Optional: some kind of rubber cushioning/bands
  * This prevents vibration sounds from the spinning fans.
  
I bought everything at amazon, just search for the names of the components. Especially take some time to choose a HEPA-Filter. A round filter would complicate the build a lot.

## Architecture
![architecure](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/architecure.png)

## Logging
You can find detailed logs for the controller inside the container using `docker logs`
It shows you the exact request it did to query Prometheus. Maybe you want to url decode it, if you want to make sure whether or not the correct query was made.
Also there is a block that shows the response from Prometheus and a block for the schedule the value fell in.
Here is an example log:
```
---------REQUEST---------
POST http://prometheus:9090/api/v1/query
Content-Type: application/x-www-form-urlencoded
Content-Length: 57

query=sum%28avg_over_time%28airfilter_dust%5B10m%5D%29%29
-----------END-----------
---------RESPONSE--------
status_code: 
200
headers: 
Content-Type: application/json
Date: Thu, 04 Jul 2019 04:53:03 GMT
Content-Length: 108
body: 
{
    "status": "success",
    "data": {
        "resultType": "vector",
        "result": [
            {
                "metric": {},
                "value": [
                    1562215983.125,
                    "5.17"
                ]
            }
        ]
    }
}
-----------END-----------
----------SCHED----------
schedule_range: WEEK_RANGE
schedule_hours: ELSE
pollution: POLLUTION2
speed: SPEED2
-----------END-----------
```
The exporter also has a request log which shows the http status requests.
```
172.21.0.7 - - [04/Jul/2019 04:59:27] "GET /sensors?ccs811=true&sds011=%2Fdev%2FttyUSB0&sleep=10 HTTP/1.1" 200 -
```

## ToDo
* Improve the exporter
  * gathering metrics for each sensor should be run in parallel
* Improve Images to not being privileged
  * Due to nasty bug in kernel up to 4.19 (latest you can go with raspi-update right now), udev rules are not hooked where i need them
* Use control wires of pwm to monitor fan health
* clean up wiring and take better pictures 
* clean up the controllers script (create function to print and activate)
* remove vunerable packages that are not needed from base docker image

## Special Thanks to
* carlosedp
  * arm exporter image
* Petr Lukas
  * For the classes of the ccs811 and hdc1080
* Scott Ellis
  * For the pwm class
