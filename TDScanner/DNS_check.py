import socket
import requests
import dns.resolver

common_str = ["www","com","cn"]
def gethost(url):
    output = ''
    if '//' in url:
        output = url.split('//')[1]
        if '/' in output:
            output = output.split('/')[0]
    elif '/' in url:
        output = url.split('/')[0]
    return output


def getip(url):
    return socket.gethostbyname(gethost(url))


#By sending HTTP requests to the target website, and then checking the status code and content of the response, if the status code is not 200 or the content is not as expected, there may be DNS Spoofing.
def check_expected_content(url):
    response = requests.get(url)
    text = response.text
    host = gethost(url)
    expect_content_split = host.split(".")
    for item in expect_content_split:
        if response.status_code == 200 and item not in common_str and item in response.text:
            return True

    return False

#Another method of verification is to use python's dnspython module to query different DNS servers and compare the returned results. If the results are inconsistent, it indicates that there may be DNS Spoofing.
def compare_different_dsn(url):
    dns_servers = ["8.8.8.8","1.1.1.1","1.0.0.1", "208.67.222.222",
                   "208.67.220.220","9.9.9.9","149.112.112.112","8.26.56.26",
                   "8.20.247.20","114.114.114.114"]  # different DNS
    results = []
    for dns_server in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        answer = resolver.resolve(gethost(url), "A")
        for item in answer:
            if item.address not in results:
                results.append(item.address)  # 获取IP地址

    return results



