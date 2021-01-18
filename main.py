import socket
# https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol
MAX_BYTES = 1024

serverPort = 67  # port destinatie=adr. MAC a clientului
clientPort = 68  # port sursa= adr. MAC a expeditorului


class DhcpServer (object):

    def server(self):
        print("DHCP server is starting...\n")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # se creaza obiecte de tip socket;  AF_INET=familia de adr. sock_dgram=socket orientat catra datagrama
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # apare o excepție după revenirea apelului de sistem, va încerca mai întâi să închidă orice descriptor de fișiere primit prin acest mecanism
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # este setată pentru a reutiliza imediat socket-urile anterioare care erau legate pe aceeași adresă și au rămas în starea TIME_WAIT
        s.bind(('', serverPort))
        dest = ('255.255.255.255', clientPort)

        while 1:
            try:
                print("Wait DHCP discovery.")
                data, address = s.recvfrom(MAX_BYTES)
                print("Receive DHCP discovery.")

                print("Send DHCP offer.")
                data = DhcpServer .offer_get()
                s.sendto(data, dest)
                while 1:
                    try:
                        print("Wait DHCP request.")
                        data, address = s.recvfrom(MAX_BYTES)
                        print("Receive DHCP request.")

                        print("Send DHCP pack.\n")
                        data = DhcpServer .pack_get()
                        s.sendto(data, dest)
                        break
                    except:
                        raise
            except:
                raise

    def offer_get(self):

        op = bytes([0x02]) # octet 0
        htype = bytes([0x01]) # octetul 1
        hlen = bytes([0x06]) #octetul 2
        hops = bytes([0x00]) #octetul 3
        xid = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])  # adr. IP a clientului
        yiaddr = bytes([0xC0, 0xA8, 0x01, 0x64])  # 192.168.1.100 adr dvs. IP
        siaddr = bytes([0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1 adr. IP a serverului
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])  # adr. gateaway
        chaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])  # adr. hardware client 
        chaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])
        chaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr5 = bytes(192)
        magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        dhcpoptions1 = bytes([53, 1, 2])  # DHCP Offer
        dhcpoptions2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])  # 255.255.255.0 masca subretea (/24)
        dhcpoptions3 = bytes([3, 4, 0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1 router
        dhcpoptions4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])  # 86400s(1 day) IP address lease time
        dhcpoptions5 = bytes([54, 4, 0xC0, 0xA8, 0x01, 0x01])  # DHCP server

        package = op + htype + hlen + hops + xid + secs + flags + ciaddr + yiaddr + siaddr + giaddr + chaddr1 + chaddr2 + chaddr3 + chaddr4 + chaddr5 + magiccookie + dhcpoptions1 + dhcpoptions2 + dhcpoptions3 + dhcpoptions4 + dhcpoptions5

        return package

    def pack_get(self):
        op = bytes([0x02])
        htype = bytes([0x01])
        hlen = bytes([0x06])
        hops = bytes([0x00])
        xid = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0xC0, 0xA8, 0x01, 0x64])
        siaddr = bytes([0xC0, 0xA8, 0x01, 0x01])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])
        chaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])
        chaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr5 = bytes(192)
        magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        dhcpoptions1 = bytes([53, 1, 5])  # DHCP ACK(value = 5)
        dhcpoptions2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])  # 255.255.255.0 subnet mask
        dhcpoptions3 = bytes([3, 4, 0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1 router
        dhcpoptions4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])  # 86400s(1 day) IP address lease time
        dhcpoptions5 = bytes([54, 4, 0xC0, 0xA8, 0x01, 0x01])  # DHCP server

        package = op + htype + hlen + hops + xid + secs + flags + ciaddr + yiaddr + siaddr + giaddr + chaddr1 + chaddr2 + chaddr3 + chaddr4 + chaddr5 + magiccookie + dhcpoptions1 + dhcpoptions2 + dhcpoptions3 + dhcpoptions4 + dhcpoptions5

        return package


if __name__ == '__main__':
    DhcpServer = DhcpServer()
    DhcpServer .server()
