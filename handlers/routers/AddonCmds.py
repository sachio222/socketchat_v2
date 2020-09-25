from addons import weather, urbandict, moon, mathfacts, map, globe, wikip


class Router():
    """Routes all add-on commands.

    **************************************************************************
    To add an Addon:
        Step 1: Import <addon>.py file. 
        Step 2: Define function (can pass in split msg_parts).
        Step 3: Add command as Key, and function name as Value to cmd_dict
        **********************************************************************
    """

    def __init__(self):
        pass

    def epic(self, *args, **kwargs):
        globe.animate()

    def mathfacts(self, msg_parts: list, *args, **kwargs):
        mathfacts.get_fact(msg_parts)

    def map(self, msg_parts: list, *args, **kwargs):
        """Input location string"""
        map.open_map(msg_parts)

    def moon(self, *args, **kwargs):
        moon.phase()

    def urband(self, msg_parts: list, *args, **kwargs):
        """Input lookup string"""
        urbandict.urbandict(msg_parts)

    def weather(self, msg_parts: list, *args, **kwargs):
        """Input location string"""
        weather.report(msg_parts)

    def wikipedia(self, msg_parts: list, *args, **kwargs):
        """Input lookup string"""
        wikip.WikiArticle().run_from_cli(msg_parts)

    dispatch_cmds = {
        '/epic': epic,
        '/map': map,
        '/mathfacts': mathfacts,
        '/moon': moon,
        '/urband': urband,
        '/weather': weather,
        '/wikipedia': wikipedia,
        '/wp': wikipedia
    }
