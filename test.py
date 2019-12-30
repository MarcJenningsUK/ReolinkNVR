from ReolinkNvr import ReolinkNvr

n = ReolinkNvr("192.168.2.130", "username", "password")
l = n.login()
print(l)

j = n.channelstatus()
print(j)

o = n.logout()
print(o)
