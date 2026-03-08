# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# add docstring to this module

"""Tools module for the maintenance scheduling agent."""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from toolbox_core import ToolboxSyncClient
from maintenance_scheduler.config import Config

config = Config()
logger = logging.getLogger(__name__)
time_zone = ZoneInfo("Europe/Berlin")

# Initialize the MCP Toolbox Client unconditionally
if not config.mcp_toolbox_uri:
    raise ValueError("mcp_toolbox_uri must be set in your configuration / .env file.")

toolbox = ToolboxSyncClient(config.mcp_toolbox_uri)

# Load the BigQuery tools directly from the MCP server
get_unresolved_incidents_tool = toolbox.load_tool('get-unresolved-incidents')
get_expected_number_of_passengers_tool = toolbox.load_tool('get-expected-number-of-passengers')
schedule_maintenance_tool = toolbox.load_tool('schedule-maintenance')


# Retain the local utility functions
def get_current_time() -> str:
    """
    Returns current time in New York, NY, USA
    """
    logger.info("Getting current time")
    return datetime.now(tz=time_zone).strftime('%a %d %b %Y, %I:%M%p')

def is_time_on_weekend(day: int, month: int, year: int) -> bool:
    """
    Returns a Boolean indicating if the current time is on the weekend
    """
    date = datetime(year, month, day)
    is_weekend = date.weekday() > 4
    logger.info("Is day a weekend: %s %s %s: %s", year, month, day, is_weekend)
    return {"is_weekend": is_weekend}