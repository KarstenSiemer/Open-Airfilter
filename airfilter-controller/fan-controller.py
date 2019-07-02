#!/usr/bin/env python3
"""This controlls the airfilter fans"""

import os
import sys
import time
import requests
import json
from pwm import PWM
from datetime import datetime
from pretty_json import format_json

def print_request(req):
    print('{}\n{}\n{}\n\n{}\n{}'.format(
        '---------REQUEST---------',
         req.method + ' ' + req.url,
         '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
         req.body,
        '-----------END-----------',
    ))

def print_response(resp):
    headers = '\n'.join(f'{k}: {v}' for k, v in resp.headers.items())
    content_type = resp.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        try:
            body = format_json(resp.json())
        except json.JSONDecodeError:
            body = resp.text
    else:
        body = resp.text

    print('{}\n{}\n{}\n{}\n{}'.format(
        '---------RESPONSE--------',
        'status_code: \n' + str(resp.status_code),
        'headers: \n' + headers,
        'body: \n' + body,
        '-----------END-----------',
        ))

def print_information(sched_range, sched_hours, pollution, speed):
    print('{}\n{}\n{}\n{}\n{}\n{}'.format(
        '----------SCHED----------',
        'schedule_range: ' + sched_range,
        'schedule_hours: ' + sched_hours,
        'pollution: ' + pollution,
        'speed: ' + speed,
        '-----------END-----------',
        ))

def main(args=None):
    if len(sys.argv) != 3:
        print('fan-controller.py << prometheus server URL >> "<< query >>" ')
        print()
        print("""Example: fan-controller.py http://prometheus:9090 'irate(http_requests_total{code="200"}[1m])'""")
        print()
        sys.exit(1)

    prometheus  = sys.argv[1]
    promquery   = sys.argv[2]

    weekrange   = range(1, int(os.environ['WEEK_RANGE']))
    workhours   = range(int(os.environ['WORK_HOURS_FROM']),    int(os.environ['WORK_HOURS_UNTIL']))
    weekhome    = range(int(os.environ['WEEK_HOME_FROM']),     int(os.environ['WEEK_HOME_UNTIL']))
    weekendhome = range(int(os.environ['WEEK_END_HOME_FROM']), int(os.environ['WEEK_END_HOME_UNTIL']))

    speed1 = int(os.environ['SPEED1'])
    speed2 = int(os.environ['SPEED2'])
    speed3 = int(os.environ['SPEED3'])
    speed4 = int(os.environ['SPEED4'])
    speed5 = int(os.environ['SPEED5'])
    speed6 = int(os.environ['SPEED6'])

    pollution1 = int(os.environ['POLLUTION1'])
    pollution2 = int(os.environ['POLLUTION2'])
    pollution3 = int(os.environ['POLLUTION3'])
    pollution4 = int(os.environ['POLLUTION4'])
    pollution5 = int(os.environ['POLLUTION5'])
    pollution6 = int(os.environ['POLLUTION6'])

    pwm0 = PWM(0)
    pwm1 = PWM(1)

    pwm0.export()
    pwm1.export()

    pwm0.period = int(os.environ['PWM0_PERIOD'])
    pwm1.period = int(os.environ['PWM1_PERIOD'])

    while True:
        req = requests.Request('POST', prometheus + '/api/v1/query', headers={'Content-Type': 'application/x-www-form-urlencoded'},data={'query': promquery})
        prepared = req.prepare()
        print_request(prepared)

        session = requests.Session()
        response = session.send(prepared)
        print_response(response)

        results = response.json()['data']['result']

        for result in results:
            day   = datetime.utcfromtimestamp(int(result['value'][0])).strftime('%w')
            hour  = datetime.utcfromtimestamp(int(result['value'][0])).strftime('%H')
            value = float(result['value'][1])

            if int(day) in weekrange:
                if int(hour) in workhours:
                    print_information("WEEK_RANGE", "WORK_HOURS", "DISABLED", "DISABLED")
                    pwm0.enable = False
                    pwm1.enable = False
                elif int(hour) in weekhome:
                    if value > pollution6:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION6", "SPEED6")
                        pwm0.duty_cycle = speed6
                        pwm1.duty_cycle = speed6
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution5:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION5", "SPEED5")
                        pwm0.duty_cycle = speed5
                        pwm1.duty_cycle = speed5
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution4:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION4", "SPEED4")
                        pwm0.duty_cycle = speed4
                        pwm1.duty_cycle = speed4
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution3:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION3", "SPEED3")
                        pwm0.duty_cycle = speed3
                        pwm1.duty_cycle = speed3
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution2:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION2", "SPEED2")
                        pwm0.duty_cycle = speed2
                        pwm1.duty_cycle = speed2
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution1:
                        print_information("WEEK_RANGE", "WORK_HOME", "POLLUTION1", "SPEED1")
                        pwm0.duty_cycle = speed1
                        pwm1.duty_cycle = speed1
                        pwm0.enable = True
                        pwm1.enable = True
                    else:
                        print_information("WEEK_RANGE", "WORK_HOME", "DISALBED", "DISABLED")
                        pwm0.enable = False
                        pwm1.enable = False
                else:
                    if value > pollution2:
                        print_information("WEEK_RANGE", "ELSE", "POLLUTION2", "SPEED2")
                        pwm0.duty_cycle = speed2
                        pwm1.duty_cycle = speed2
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution1:
                        print_information("WEEK_RANGE", "ELSE", "POLLUTION1", "SPEED1")
                        pwm0.duty_cycle = speed1
                        pwm1.duty_cycle = speed1
                        pwm0.enable = True
                        pwm1.enable = True
                    else:
                        print_information("WEEK_RANGE", "ELSE", "DISABLED", "DISABLED")
                        pwm0.enable = False
                        pwm1.enable = False
            else:
                if int(hour) in weekendhome:
                    if value > pollution6:
                        print_information("WEEK_END", "HOME", "POLLUTION6", "SPEED6")
                        pwm0.duty_cycle = speed6
                        pwm1.duty_cycle = speed6
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution5:
                        print_information("WEEK_END", "HOME", "POLLUTION5", "SPEED5")
                        pwm0.duty_cycle = speed5
                        pwm1.duty_cycle = speed5
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution4:
                        print_information("WEEK_END", "HOME", "POLLUTION4", "SPEED4")
                        pwm0.duty_cycle = speed4
                        pwm1.duty_cycle = speed4
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution3:
                        print_information("WEEK_END", "HOME", "POLLUTION3", "SPEED3")
                        pwm0.duty_cycle = speed3
                        pwm1.duty_cycle = speed3
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution2:
                        print_information("WEEK_END", "HOME", "POLLUTION2", "SPEED2")
                        pwm0.duty_cycle = speed2
                        pwm1.duty_cycle = speed2
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution1:
                        print_information("WEEK_END", "HOME", "POLLUTION1", "SPEED1")
                        pwm0.duty_cycle = speed1
                        pwm1.duty_cycle = speed1
                        pwm0.enable = True
                        pwm1.enable = True
                    else:
                        print_information("WEEK_END", "HOME", "DISABLED", "DISABLED")
                        pwm0.enable = False
                        pwm1.enable = False
                else:
                    if value > pollution2:
                        print_information("WEEK_END", "ELSE", "POLLUTION2", "SPEED2")
                        pwm0.duty_cycle = speed2
                        pwm1.duty_cycle = speed2
                        pwm0.enable = True
                        pwm1.enable = True
                    elif value > pollution1:
                        print_information("WEEK_END", "ELSE", "POLLUTION1", "SPEED1")
                        pwm0.duty_cycle = speed1
                        pwm1.duty_cycle = speed1
                        pwm0.enable = True
                        pwm1.enable = True
                    else:
                        print_information("WEEK_END", "ELSE", "DISALBED", "DISABLED")
                        pwm0.enable = False
                        pwm1.enable = False

        time.sleep(30)

if __name__ == "__main__":
    main()
