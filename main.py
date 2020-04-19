from flask import Flask , request
import configparser
from twilio.twiml.messaging_response import MessagingResponse
import coronaDataset

app = Flask(__name__)


rawdata = open('template.txt')
tmplt = rawdata.read()


@app.route("/")
def hello():
    return "Hello, World!"


def getOverallSummary(overallSummary):

    content_msg = ''

    keys = overallSummary.keys()

    for key in keys:
        updatedDataset = open("sentMSG.txt" , "a")
        updatedDataset.write(key + ': {}'.format(overallSummary[key])+'\n')
        updatedDataset.close()


def getOverallregionalstats(overallregionalstats):
    states=len(overallregionalstats)
    updatedDataset = open("sentMSG.txt" , "a")
    for state in overallregionalstats[:11]:
        keys = state.keys()
        updatedDataset.write('\n')
        for key in keys:

            updatedDataset.write(key + ': {}'.format(state[key]) + '\n')
    updatedDataset.close()


def getLastRefreshed(lastRefreshed):
    from datetime import datetime
    from dateutil import tz


    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    utc = datetime.strptime(lastRefreshed.replace('T',' ').split('.')[0], '%Y-%m-%d %H:%M:%S')
    
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)

    updatedDataset = open("sentMSG.txt" , "a")
    updatedDataset.write('last updated data is on {} \n\n'.format(central.ctime()))
    updatedDataset.close()

    return 0





@app.route("/sms" , methods=['POST'])
def sms_reply():
    updatedDataset = open("sentMSG.txt" , "a")
    updatedDataset.truncate(0)
    updatedDataset.close()
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    overallSummary , overallregionalstats , lastRefreshed , lastOriginUpdate = coronaDataset.getLatestCoronaUpdate()

    # msg=str(total)+str(confirmedCases)+str(confirmedCasesForeignIndian)+str(deaths)

    # total , confirmedCases , confirmedCasesForeignIndian , deaths = overallSummary['total'] , overallSummary[
    #     'confirmedCasesForeign'] , overallSummary['confirmedCasesIndian'] , overallSummary['deaths']
    # 
    # msg = ''

    getLastRefreshed(lastRefreshed)

    getOverallSummary(overallSummary)

    getOverallregionalstats(overallregionalstats)

    updatedDataset = open("sentMSG.txt")
    updatedData=updatedDataset.read()

    print(updatedData)


    # Create reply
    resp = MessagingResponse()

    resp.message(updatedData)

    return str(resp)


if __name__ == "__main__":

    app.run(debug=True)
