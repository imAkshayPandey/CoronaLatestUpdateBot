


def checkNetworkStatus(fetched_data):

    return fetched_data['success']



def getLatestCoronaUpdate():
    import requests

    url = 'https://api.rootnet.in/covid19-in/stats/latest'
    r = requests.get(url)

    fetched_data = r.json()
    if checkNetworkStatus(fetched_data):
        data=fetched_data['data']
        overallSummary=data['summary']
        overallregionalstats=data['regional']

        lastRefreshed=fetched_data['lastRefreshed']
        lastOriginUpdate=fetched_data['lastOriginUpdate']



        return overallSummary,overallregionalstats,lastRefreshed,lastOriginUpdate
    else:

        return str("couldn't fetch latest data")



if __name__=='__main__':
    getLatestCoronaUpdate()