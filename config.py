#!/usr/bin/env python3
# Copyright (c) LittleFish Corporation. All rights reserved.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 5050
    APP_ID = os.environ.get("MicrosoftAppId", "6428c0c4-a221-4c8a-ab80-86e4ff01e086")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "EpJ8Q~hTO5ZMbL~bC2xmx0JuViU9hH2FLz3MnbYg")
