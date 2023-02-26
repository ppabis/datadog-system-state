import os, shutil
from datetime import datetime
from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

__version__ = "0.1.0"
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
    
    def get_days_since_last_reboot(self):
        out, _, _ = get_subprocess_output(["uptime", "-s"], self.log)
        boot_time = datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - boot_time).days

    def get_os_major_version(self):
        version = "-1"
        # Using lsb_release binary if present
        if shutil.which("lsb_release") is not None:
            out, _, _ = get_subprocess_output(["lsb_release", "-rs"], self.log)
            version = out
        # Using /etc/lsb-release file if present
        elif os.path.isfile("/etc/lsb-release"):
            with open("/etc/lsb-release", "r") as f:
                for line in f:
                    if line.startswith("DISTRIB_RELEASE="):
                        version = line.split("=")[1]
                        break
        # Using /etc/os-release file if present
        elif os.path.isfile("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("VERSION_ID="):
                        version = line.split("=")[1]
                        break
        
        return int( version.strip('"').split(".")[0] )


    def check(self, instance):
        tags = instance.get('tags', [])
        self.gauge('systemstate.upgradable_packages', self.get_upgradable_packages(), tags=tags)
        self.gauge('systemstate.days_since_last_reboot', self.get_days_since_last_reboot(), tags=tags)
        self.gauge('systemstate.os_major_version', self.get_os_major_version(), tags=tags)