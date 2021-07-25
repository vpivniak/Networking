from IPv4Address.IPv4Address import IPv4Address


class Network(object):
    ALL_ONES = 0xFFFFFFFF

    def __init__(self, address, mask_length):
        if mask_length > 32 or mask_length < 1:
            raise ValueError("Invalid mask")
        self._mask_length = mask_length
        self._address = IPv4Address(address.ip & self.netmask)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = IPv4Address(address.ip & self.netmask)

    @property
    def mask_length(self):
        return self._mask_length

    @mask_length.setter
    def mask_length(self, mask_length):
        self._mask_length = mask_length

    @property
    def wildcard_mask(self):
        return Network.ALL_ONES & (Network.ALL_ONES >> self.mask_length)

    @property
    def netmask(self):
        return self.wildcard_mask ^ Network.ALL_ONES

    @property
    def broadcast_address(self):
        return IPv4Address(self.address.ip | self.wildcard_mask)

    @property
    def first_usable_address(self):
        if self.mask_length == 31:
            raise Exception("Point ot point link")
        if self.mask_length == 32:
            return self.address
        return IPv4Address((self.address.ip & self.netmask) + 1)

    @property
    def last_usable_address(self):
        if self.mask_length == 31:
            raise Exception("Point to point link")
        if self.mask_length == 32:
            return IPv4Address(self.address.ip + self.broadcast_address.ip)
        return IPv4Address(self.broadcast_address.ip - 1)

    @property
    def mask_string(self):
        return self.to_string()

    @property
    def total_hosts(self):
        return (self.last_usable_address.ip - self.first_usable_address.ip) + 1

    @property
    def subnets(self):
        subnet = []
        subnet.append(Network(self.address, self.mask_length + 1))
        subnet.append(Network(IPv4Address(subnet[0].broadcast_address.ip + 1),
                              self.mask_length + 1))
        return subnet

    def to_string(self):
        octet1 = self.netmask >> 24
        octet2 = (self.netmask >> 16) & 255
        octet3 = (self.netmask >> 8) & 255
        octet4 = self.netmask & 255
        return f'{octet1}.{octet2}.{octet3}.{octet4}'

    def __contains__(self, address):
        return self.broadcast_address > address > self.address

    @property
    def is_public(self):
        return self.address in CLASS_A or \
               self.address in CLASS_B or \
               self.address in CLASS_C

    def __str__(self):
        return f'{self.address}/{self.mask_length}'


CLASS_A = Network(IPv4Address('10.0.0.0'), 8)
CLASS_B = Network(IPv4Address('172.16.0.0'), 12)
CLASS_C = Network(IPv4Address('192.168.0.0'), 16)

if __name__ == '__main__':
    ip = IPv4Address("192.168.0.5")
    net = Network(ip, 24)

    ip2 = net.broadcast_address
    ip3 = net.first_usable_address
    ip4 = net.last_usable_address

    print(net)
    print(ip2)
    print(ip3)
    print(ip4)
    print(net.address)
    print(net.mask_string)
    print(net.mask_length)
    print(net.address)
    print(net.is_public)
    print((IPv4Address("10.0.23.4")) in net)
    print((IPv4Address("192.168.0.25")) in net)
    print(net.total_hosts)
    sub = net.subnets

    print("---------------\n First subnet")

    print(sub[0].address)
    print(sub[0].first_usable_address)
    print(sub[0].last_usable_address)
    print(sub[0].mask_length)

    print("---------------\n Second subnet")

    print(sub[1].address)
    print(sub[1].first_usable_address)
    print(sub[1].last_usable_address)
    print(sub[1].mask_length)
