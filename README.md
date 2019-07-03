# Open-Airfilter
Opensource airfiltering system for your home

Since i have problems with pollen in summer i wanted to buy an airfiltering system, but failed to find one that suits my needs.
Like being extremly silent or setting up schedules on when i want it to not run or that it should be even more silent when i want to go to sleep.

That is why i decided to just create my own and of course share my work.

Here are two pictures of it. (as an excuse, i am really not talented when it comes to working with wood)
![front view of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture1.jpg)
![insides of the filter](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/picture2.jpg)

This is how your grafana dashboard will look like:
* coming soon

## How to wire it up
* coming soon

## How configure
* coming soon

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
![architecure](https://github.com/KarstenSiemer/Open-Airfilter/raw/master/pictures/architecture.png)

## ToDo
* Improve the exporter
  * gathering metrics for each sensor should be run in parallel
* Improve Images
  * Due to nasty bug in kernel up to 4.19 (latest you can go with raspi-update right now), udev rules are not hooked where i need them

## Special Thanks to
* carlosedp
  * for supplying prometheus, node- and arm exporter images for the armv7l architecture
* Petr Lukas
  * For the classes of the ccs811 and hdc1080
* Scott Ellis
  * For the pwm class
