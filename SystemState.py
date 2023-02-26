import os, shutil
from datetime import datetime
from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

class SystemState(AgentCheck):

    def get_upgradable_packages(self):
        # Debian
        if shutil.which("apt") is not None:
            cmd = ["apt", "-qq", "list", "--upgradable"]
        # RedHat
        elif shutil.which("dnf") is not None:
            cmd = ["dnf", "-q", "check-update"]
        else:
            return -1 # Not supported
        
        out, _, _ = get_subprocess_output(cmd, self.log)
        
        return len( # Count the lines (wc -l)
         list( # Convert to list
          filter( # Filter out empty lines (grep -v ^$)
           lambda x: len(x) > 0, out.splitlines()
           )
         )
        )

    def check(self, instance):
        pass