#!/bin/bash
source /home/mostaq/PycharmProjects/SmsService/venv/bin/activate
python /home/mostaq/PycharmProjects/SmsService/general_queue.py R,1
python /home/mostaq/PycharmProjects/SmsService/campaign_queue.py R,1