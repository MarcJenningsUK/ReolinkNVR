from ReolinkNvr import ReolinkNvr, AttachedCamera
import json

n = ReolinkNvr("192.168.2.130", "username", "password")
l = n.login()
#print(l)
cams = []

j = n.getchannelstatus()
# print(j)
data = json.loads(j)
for val in data[0]["value"]["status"]:
    c1 = AttachedCamera(val["channel"], val["online"] == 1)
    #if(c1.online):
    cams.append(c1)

for cam in cams:
    print("Channel", cam.channel, cam.online)

o = n.logout()
#print(o)




