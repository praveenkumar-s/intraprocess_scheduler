import requests

def online(VM):
    requests.get('http://localhost:5000/vm/bring_online/{0}'.format(VM))
    print("Done"+VM+" is online !")


def offline(VM):
    requests.get('http://localhost:5000/vm/bring_offline/{0}'.format(VM))
    print("Done"+VM+" is offline !")