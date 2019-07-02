# Open-Airfilter
Opensource airfiltering system for your home

Since i have problems with pollen in summer i wanted to buy an airfiltering system, but failed to find one that suits my needs.
Like being extremly silent or setting up schedules on when i want it to not run or that it should be even more silent when i want to go to sleep.

That is why i decided to just create my own and of course share my work.

Here are two pictures of it. (as an excuse, i am really not talented when it comes to working with wood)


What i have used to build this:
* raspberry pi 3 b+
  * this is overpowered for an airfilter, but i chose to put the whole stack on it, so it needs at least some beef
* Noctua NF-A14 5V PWM
  * I chose this because i do not have to change voltage to use it
  * You can use any fan of any size, just make sure that it can be used it PWM
* Nova PM Sensor SDS011 High Precision PM2.5
  * Most accurate sensor on consumer maket (to my knowledge)
  * But it has the downside that it needs a fan to suck fresh air into it's chamber (sadly, i can hear it sometimes)
  * also take some tubing to elongate the the rod where it sucks in air, so you can directly suck from the airflow of the fans 
* 140mm fan grill
  * for the backside of the airfilter to fight of hughe dust particles and protect the inside wiring
* HEPA-Filter
  * mine is square (17 x 17 x 6 cm)
* some eva feed to put the wooden box on
* a box to place the components in (i used wood)
* optional: CCS811 HDC1080 sensor
  * nice way to get even more information about the air you breath in every day.
