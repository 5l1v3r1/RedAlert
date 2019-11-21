from elastalert.alerts import Alerter, BasicMatchString
import os
from slack import WebClient

class SlackPasswordAlerter(Alerter):

    def __init__(self, rule):
        super(SlackPasswordAlerter, self).__init__(rule)
        self.sk = os.environ.get('SLACK_KEY')    # get slack api key
        self.scn = os.environ.get('SLACK_CHANNEL_NAME', 'password-alerts')     # get channel name

    def send_slack_msg(self, sendstr):
        tok = self.sk
        sc = WebClient(token=tok)  
        channels = sc.channels_list(exclude_archived=1)
        for ch in channels:
            if ch.get('name') == self.scn:
                scid = ch.get('id')
                break
            else:
                scid = ""
        sc.chat_postMessage(
            channel=scid,
            text=sendstr
        )
        return

    # Alert is called
    def alert(self, matches):

        # Matches is a list of match dictionaries.
        # It contains more than one match when the alert has
        # the aggregation option set
        for match in matches:
                # basic_match_string will transform the match into the default
                # human readable string format
                match_string = "rotating_light: :rotating_light: " + str(BasicMatchString(self.rule, match))
                self.send_slack_msg(match_string)
                #output_file.write(match_string)

    # get_info is called after an alert is sent to get data that is written back
    # to Elasticsearch in the field "alert_info"
    # It should return a dict of information relevant to what the alert does
    def get_info(self):
        return {'type': 'Slack Password Alerter',
                'Slack Channel': self.scn}

    