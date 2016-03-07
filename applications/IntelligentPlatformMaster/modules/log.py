# Copyright 2015 China Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2010 Aostarit Foundation
# All Rights Reserved.
#
#    Licensed under the Aostarit License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.aostarit.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function
import logging

_loggers = {}

def getLogger(name='unknown'):
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]

class WritableLogger(object):
    """A thin wrapper that responds to `write` and logs."""

    def __init__(self, logger, level=logging.DEBUG):
        self.logger = logger
#        self.level = logging.getLevelName(CONF.log.level)
        self.level = level

    def write(self, msg):
        self.logger.log(self.level, msg.rstrip())