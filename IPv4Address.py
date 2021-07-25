class InvalidIP(Exception):
    pass


class IPv4Address(object):
    def __init__(self, ip='127.0.0.1'):
        if isinstance(ip, str):
            self.ip = ip
            self.ip = int(self)
        elif isinstance(ip, int):
            self.validate_ip_int(ip)
            self.ip = ip
        else:
            raise InvalidIp

    def validate_ip_int(self, ip):
        if ip < 0 or ip > 0xFFFFFFFF:
            raise InvalidIp

    def __str__(self):
        if not isinstance(self.ip, str):
            print(f'int {self.ip}')
            octet1 = self.ip >> 24
            print(octet1)
            octet2 = (self.ip >> 16) & 255
            print(octet2)
            octet3 = (self.ip >> 8) & 255
            print(octet3)
            octet4 = self.ip & 255
            print(octet4)
            return "{}.{}.{}.{}".format(octet1, octet2, octet3, octet4)
        else:
            return self.ip

    def __int__(self):
        if not isinstance(self.ip, int):
            print(f'str {self.ip}')
            octets = self.ip.split('.')
            if len(octets) != 4:
                raise InvalidIp
            for octet in octets:
                if int(octet) < 0 or int(octet) > 255:
                    raise InvalidIp()
            return (int(octets[0]) << 24) + \
                   (int(octets[1]) << 16) + \
                   (int(octets[2]) << 8) + \
                   int(octets[3])
        else:
            return self.ip

    def __lt__(self, address):
        return self.ip < address.ip

    def __gt__(self, address):
        return self.ip > address.ip

    def __le__(self, address):
        return self.ip <= address.ip

    def __ge__(self, address):
        return self.ip >= address.ip

    def __eq__(self, address):
        return self.ip == address.ip

    def __ne__(self, address):
        return not self.__eq__(address)


if __name__ == '__main__':
    ip = IPv4Address('127.12.45.22')
    print(ip)
    print(int(ip))

    ip = IPv4Address(2131505409)
    print(ip)
    print(int(ip))

    print(ip == IPv4Address("127.12.45.22"))
    print(ip == IPv4Address(2131504406))
    print(ip == IPv4Address(0xF834AD02))
    print(ip != IPv4Address("189.11.23.211"))

    print(ip > IPv4Address('131.16.34.66'))
    print(ip < IPv4Address('131.16.34.66'))
