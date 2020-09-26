from addons import weather, urbandict, moon, mathfacts, maps, globe, wikip

"""Routes all add-on commands.

**************************************************************************
To add an Addon:
    Step 1: Import <addon>.py file. 
    Step 2: Define function (can pass in split msg_parts).
    Step 3: Add command as Key, and function name as Value to cmd_dict
    **********************************************************************
"""

def run_epic(*args, **kwargs):
    globe.animate()

def run_mathfacts(*args, **kwargs):
    msg_parts = kwargs["msg_parts"]
    mathfacts.get_fact(msg_parts)

def run_maps(*args, **kwargs):
    """Input location string"""
    msg_parts = kwargs["msg_parts"]
    maps.open_map(msg_parts)

def run_moon(*args, **kwargs):
    moon.phase()

def run_urband(*args, **kwargs):
    """Input lookup string"""
    msg_parts = kwargs["msg_parts"]
    urbandict.urbandict(msg_parts)

def run_weather(*args, **kwargs):
    """Input location string"""
    msg_parts = kwargs["msg_parts"]
    weather.report(msg_parts)

def run_wikipedia(*args, **kwargs):
    """Input lookup string"""
    msg_parts = kwargs["msg_parts"]
    wikip.WikiArticle().run_from_cli(msg_parts)

dispatch_cmds = {
    '/epic': run_epic,
    '/map': run_maps,
    '/mathfacts': run_mathfacts,
    '/moon': run_moon,
    '/urband': run_urband,
    '/weather': run_weather,
    '/wikipedia': run_wikipedia,
    '/wp': run_wikipedia
}