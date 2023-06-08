import appdaemon.plugins.hass.hassapi as hass
from steamgifts_autoenter import SteamgiftsAutoenter

class SteamgiftsAutoenterAppDaemon(hass.Hass):
    
    def initialize(self):
        self.app = SteamgiftsAutoenter(self.args["username"], self.args["password"], self.args["cookies_file"], self.args["blacklist"], self.log)
        event = self.args["launch_event"]
        self.listen_event(self.run , event = event)
        self.log(f"Listening for event {event}")
        for time in self.args["scheduled_run"]:
            self.log(f"Scheduling run at {time}")
            self.run_at(self.run, time)

    def run(self, *kwargs):
        self.app.run()