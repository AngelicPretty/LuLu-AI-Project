#!/bin/bash
nohup python bot_lulu_main.py > ./logs/nohup.out 2>&1 &
echo "======== LuLu Bot Running on http://172.17.0.2:5050 ========"
