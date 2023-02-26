import os, shutil
from datetime import datetime
from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

class SystemState(AgentCheck):
    def check(self, instance):
        pass