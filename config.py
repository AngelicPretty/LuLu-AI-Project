#!/usr/bin/env python3
# Copyright (c) LittleFish Corporation. All rights reserved.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 5050
    APP_ID = os.environ.get("MicrosoftAppId", "{APP-ID}")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "{APP-Key}")
