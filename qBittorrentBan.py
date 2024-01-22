import requests
import json
import time
import random
import math
import string
import configparser
import os

from requests import RequestException
from requests.exceptions import ConnectionError, Timeout, RequestException

def getDownloadItem(url, cookie):
    # Generate a random number
    rid = random.random() * 1000
    rid = math.floor(rid)

    param = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    content = {'rid': rid, param: ''}
    rsp = requests.get(url, params=content, headers=def_headers, cookies=cookie)
    return json.loads(str(rsp.content, 'utf-8'))['torrents']

def getTorrentHashAndStatus(torrentVal, value):
    status = value.get('state')
    if status is not None:
        status = status.lower()
        if "uploading" == status or "downloading" == status:
            return torrentVal

def queryTorrentClient(url, cookie, hashVal):
    blockList = []
    rid = random.random() * 1000
    rid = math.floor(rid)

    param = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    content = {'rid': rid, 'hash': hashVal, param: ''}

    rsp = requests.get(url, params=content, headers=def_headers, cookies=cookie)
    PeersInfo = json.loads(str(rsp.content, 'utf-8'))['peers']

    for peer in PeersInfo:
        if isNeedBlockClient(PeersInfo[peer]):
            blockList.append(PeersInfo[peer])
    return blockList

def reloadIpFilter(url, bannedIps, cookie):
    reload = {'ip_filter_enabled': True, 'banned_IPs': bannedIps}
    content = {'json': json.dumps(reload, ensure_ascii=False)}

    requests.post(url, content, headers=headers, cookies=cookie)

def getAllFilerClient(itemsHash, url, cookie):
    blockAllList = []
    for item in itemsHash:
        blockList = queryTorrentClient(url, cookie, item)
        if blockList is not None:
            blockAllList.append(blockList)
    return blockAllList

def isNeedBlockClient(peer):
    client = peer.get('client')
    if client is None:
        return False

    for deFilter in filter_rules:
        if deFilter['findType'] == 1 and client.find(deFilter['name']) > -1:
            return True
        elif deFilter['findType'] == 2 and client.startswith(deFilter['name']):
            return True

    return False

def writeToFile(newAddList):
    with open(fileAddress, 'a+') as f:
        for writeIp in newAddList:
            f.write(writeIp + '\n')
        f.close()

def readExistIp():
    try:
        with open(fileAddress, 'r') as f1:
            existFilerClient = f1.readlines()
    except FileNotFoundError:
        # Create a new file if it doesn't exist
        with open(fileAddress, 'a+'):
            pass
        existFilerClient = []

    return existFilerClient

def notExistIp(existFilerClient, ipsCollect):
    newAddList = []
    for ip in ipsCollect:
        if ''.join(existFilerClient).strip('\n').find(ip['ip']) == -1:
            newAddList.append(ip['ip'])
            print("find new client: " + ip['ip'] + '\t\t' + ip['client'])
    return newAddList

def is_qBittorrent_connected(api_url):
    global cookie_jar, is_network_error

    try:
        response = requests.get(api_url, cookies=cookie_jar, timeout=5)
        response.raise_for_status()
        if is_network_error:
            print("Network connection has been restored!")
            is_network_error = False
        return True
    except requests.exceptions.RequestException as e:
        print(f"Connection to qBittorrent is abnormal, waiting for retry: {e}")
        is_network_error = True
        return False

def parse_filter_rules(config):
    filter_rules = []
    for key in config['FilterRules']:
        name, find_type = config['FilterRules'][key].split(',')
        filter_rules.append({'name': name, 'findType': int(find_type)})
    return filter_rules

if __name__ == "__main__":

    # Check if the configuration file exists, if not, create an initial configuration file
    config_file_path = 'config.ini'
    if not os.path.exists(config_file_path):
        config = configparser.ConfigParser()

        # Set default username and password
        config['Credentials'] = {'username': 'admin', 'password': 'adminadmin'}

        # Set default root URL
        config['URLs'] = {'root_url': 'https://www.qbittorrent.org'}

        # Set default file path
        config['Paths'] = {'ip_filter_file': 'ipfilter.dat'}

        # Set default filter rules
        config['FilterRules'] = {
                '; comment': 'Filter rules for blocking clients',
                '; format': 'Each rule is defined with the format: name,findType',
                '; findType': 'where findType is 1 for contains matching, 2 for prefix matching',
                            'rule_1': '-XL0012,1',
                            'rule_2': '-XL0012-,1',
                            'rule_3': 'Xunlei,1',
                            'rule_4': 'Xfplay,1',
                            'rule_5': 'go.torrent,1',
                            'rule_6': 'QQDownload,1',
                            'rule_7': '7.,2'}

        # Write to the configuration file
        with open(config_file_path, 'w') as config_file:
            config.write(config_file)

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Get username and password
    username = config.get('Credentials', 'username')
    password = config.get('Credentials', 'password')

    # Get root URL
    root_url = config.get('URLs', 'root_url')
    
    # Get file path
    fileAddress = config.get('Paths', 'ip_filter_file')

    # Get filter rules
    filter_rules = parse_filter_rules(config)

    # Login interface
    login_url = root_url + '/api/v2/auth/login'
    # Get currently downloading or uploading items
    mainData_url = root_url + '/api/v2/sync/maindata'
    # Get users connected to download files
    peers_url = root_url + '/api/v2/sync/torrentPeers'
    # Set effective interface
    filter_url = root_url + '/api/v2/app/setPreferences'

    api_url = root_url + '/api/v2/app/version'

    is_network_error = False  # Global variable to mark whether the network connection is abnormal

    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.70 Safari/537.36 '
    }

    def_headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.70 Safari/537.36 '
    }

    # Web UI login username and password
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(login_url, data, headers=headers)

    # Exit if login error occurs
    if response.text != 'Ok.':
        exit(0)

    cookie_jar = response.cookies
    # Enter the continuous running loop

    print('Filter is successfully running...')
    while True:
        if not is_qBittorrent_connected(api_url):
            time.sleep(10)  # Retry after waiting for 10 seconds
            continue
        downItem = getDownloadItem(mainData_url, cookie_jar)
        downloadList = []
        for torrent in downItem:
            hashKey = getTorrentHashAndStatus(torrent, downItem[torrent])
            if hashKey is not None:
                downloadList.append(hashKey)

        allFilerClientList = getAllFilerClient(downloadList, peers_url, cookie_jar)
        clients = [y for x in allFilerClientList for y in x]

        existIps = readExistIp()
        newList = notExistIp(existIps, clients)

        if len(newList) > 0:
            writeToFile(newList)
            ips = ''.join(existIps) + '\n'.join(newList)
            # print(ips)
            reloadIpFilter(filter_url, ips, cookie_jar)

        # Execute every 3 seconds
        time.sleep(3)
