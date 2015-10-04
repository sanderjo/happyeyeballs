import socket
import time
import ssl

# Python implementation of RFC 6555 / Happy Eyeballs: find the fastest IPv4/IPv6 connection
# See https://tools.ietf.org/html/rfc6555


def happyeyeballs(HOST, **kwargs):
    try:
        PORT=kwargs['port']
    except:
        PORT=80
    try:
        SSL=kwargs['ssl']
    except:
        SSL=False
    try:
        DEBUG=kwargs['debug']
    except:
        DEBUG=False

    shortesttime = 10000000	# something very big
    fastserver = None

    if DEBUG: print "Checking", HOST, PORT, "SSL:", SSL, "DEBUG:", DEBUG
    try:
        allinfo = socket.getaddrinfo(HOST, 80, 0, 0, socket.IPPROTO_TCP)
    except:
        if DEBUG: print "Could not resolve", HOST
        return None

    for i in allinfo:
        address = i[4][0]
        if DEBUG: print "Address is ", address
        # note: i[0] contains socket.AF_INET or socket.AF_INET6

        try:
            start = time.clock()
            # CREATE SOCKET
            s = socket.socket(i[0], socket.SOCK_STREAM)
            s.settimeout(2)
            if not SSL:
                s.connect((address, PORT))
                s.close()
            else:
                # WRAP SOCKET
                wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)    
                # CONNECT
                wrappedSocket.connect((address, PORT))
                # CLOSE SOCKET CONNECTION
                wrappedSocket.close()

            delay = 1000.0*(time.clock() - start)
            if DEBUG: print "Connecting took:", delay, "msec"
            if delay < shortesttime:
                shortesttime = delay
                fastserver = address
        except:
            if DEBUG: print "Something went wrong (possibly just no connection)"
            pass
    if DEBUG: print "Fastest server is", fastserver
    return fastserver



if __name__ == '__main__':
    print happyeyeballs('www.google.com', debug=True), "\n"

    print happyeyeballs('news-eu-ssl.newsgroupdirect.com', port=119, debug=True), "\n"
    print happyeyeballs('news-eu-ssl.newsgroupdirect.com', port=563, ssl=True, debug=True), "\n"

    print happyeyeballs('news-ssl.newsgroupdirect.com', port=119, debug=True), "\n"
    print happyeyeballs('news-ssl.newsgroupdirect.com', port=563, ssl=True, debug=True), "\n"

    print happyeyeballs('us.sslusenet.com', port=119, debug=True), "\n"
    print happyeyeballs('us.sslusenet.com', port=563, ssl=True, debug=True), "\n"


    #print happyeyeballs('', debug=True), "\n"


