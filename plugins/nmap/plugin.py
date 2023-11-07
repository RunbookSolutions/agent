# File: /plugins/nmap/plugin.py
import nmap
from agent.base_plugin import BasePlugin

class Plugin(BasePlugin):

    async def should_handle(self, event):
        if event['plugin'] == "nmap" and 'target' in event:
            return True
        return False

    def handle(self, event):
        target = event['target']

        self.agent.output.info(f"Running NMAP scan on target: {target}")

        # Create an NmapScanner instance
        nm = nmap.PortScanner()

        # Perform a simple ping scan
        nm.scan(hosts=target, arguments='-sn')

        # Get scan results
        scan_results = nm.all_hosts()

        self.agent.output.success("NMAP Scan Results:")
        for host in scan_results:
            self.agent.output.success(f"Host: {host}, Status: {nm[host].state()}")
            # You can print additional scan information as needed

        return super().handle(event)

    def teardown(self):
        return super().teardown()
