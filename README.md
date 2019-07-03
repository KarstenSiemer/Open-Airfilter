# Open-Airfilter
Opensource airfiltering system for your home

Since i have problems with pollen in summer i wanted to buy an airfiltering system, but failed to find one that suits my needs.
Like being extremly silent or setting up schedules on when i want it to not run or that it should be even more silent when i want to go to sleep.

That is why i decided to just create my own and of course share my work.

Here are two pictures of it. (as an excuse, i am really not talented when it comes to working with wood)
![front view of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture1.jpg)
![insides of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture2.jpg)

This is how your grafana dashboard will look like:
![grafana screenshot dust graphs](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/grafana-airfilter.png)
Here you can see the most important graphs. One with the raw data that has been gathered by prometheus and the other were this
data is summed and averaged. This is done so that i have a singular point of orientation of how fast (or even at all) i want to spin the fans. Prometheus makes creating such data very easy. The query for this looks like this right now:

`sum(avg_over_time(airfilter_dust[10m]))`

Which just means to take a range vector of five minutes of all instances of the metric `airfilter_dust`, of which there are two (pm 2,5 and 10) and calculate an average for each scrape point. Then sum the results together.

You could create queries that include data of more sensors and calculate the AQI (Air quality Index) for example and control your fans based on that. But i have found that to be unnecessary, since the only stuff i can filter is dust anyway.
You could however add an alertmanager to the docker-compose manifest and create prometheus alerts if some gas concentration is too high and send yourself an alert to open a window. 

If you also use the ccs811 sensor there are already dashboards prepared to monitor humidity, temperature, eco2 (equivalent calculated carbon-dioxide, within a range of 400 to 8192 parts per million (ppm)) and tvoc (Total Volatile Organic Compound) concentration within a range of 0 to 1187 parts per billion (ppb))

## How to wire it up
* coming soon

## How configure
The main configuration can be done in `/airfilter-manifest/docker-compose.yaml`
Here you can configure the fan controller in the service `airfilterfancontroller`

In `command` the second argument given to the python script is the query that the controller will use to get information from prometheus on how polluted the air is.

In the environment variables you can set:
* The [periods](https://en.wikipedia.org/wiki/Pulse-width_modulation) of your fans
* The time ranges for the modes
* The speed of your fans in six levels
* When an amount of pollution maps to which level

Also you can configure the targets of the prometheus in `/airfilter-manifest/prometheus/prometheus.yml`
Important here are the parameters with which prometheus is scraping the exporter, becauset they are actively configuring it.
There are three options here:
* sds011
  * where can the exporter find the sds011 sensor (Default: '/dev/ttyUSB0')
* sleep
  * This controlls how long the fan spins inside the sds011 sensor chamber before a measurement is made.
  * Generally you want a time that is long enough to exchange all the air in the chamber for accurate measurements (Default: 15)
* ccs811
  * This activates the optional ccs811 sensor
You can also change the retentiontime of the prometheus, currently set is the default of 200h
  
You can also build the containers yourself (Dockerfiles are included) and directly set the environment variables inside the containers, if you happen to not wanting to use docker-compose
  
## What i have used to build this:
* Raspberry pi 3 b+
  * This is overpowered for an airfilter, but i chose to put the whole stack on it, so it needs at least some beef
* Noctua NF-A14 5V PWM
  * I chose this because i do not have to change voltage to use it
  * You can use any fan of any size, just make sure that it can be used it PWM
* Nova PM Sensor SDS011 High Precision PM2.5
  * Most accurate sensor on consumer maket (to my knowledge)
  * But it has the downside that it needs a fan to suck fresh air into it's chamber (sadly, i can hear it sometimes)
  * Also take some tubing to elongate the the rod where it sucks in air, so you can directly suck from the airflow of the fans
* 140mm fan grill
  * For the backside of the airfilter to fight of hughe dust particles and protect the inside wiring
* HEPA-Filter
  * Mine is square (17 x 17 x 6 cm)
* Some eva feed to put the wooden box on
* A box to place the components in (i used wood)
* Optional: CCS811 HDC1080 sensor
  * Nice way to get even more information about the air you breath in every day.
* Optional: Breadboard
  * I added in advance, just in case i want to add more sensors

## Architecture
![architecure](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/architecure.png)

## ToDo
* Improve the exporter
  * gathering metrics for each sensor should be run in parallel
* Improve Images to not being privileged
  * Due to nasty bug in kernel up to 4.19 (latest you can go with raspi-update right now), udev rules are not hooked where i need them

## Special Thanks to
* carlosedp
  * for supplying prometheus, node- and arm exporter images for the armv7l architecture
* Petr Lukas
  * For the classes of the ccs811 and hdc1080
* Scott Ellis
  * For the pwm class
