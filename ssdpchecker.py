# coding: EUC_JP

import sys,re
import socket,threading
from csvloader import CsvData

class SSDP_Analizer:
    def __init__(self,fname):
        self.fname = fname
        self.ip2ptr = {}

    def showinfo(self):
        print("Filename: %s"%(self.fname))

    def load(self, thre=0):
        self.thre = int(thre)
        dl = CsvData(self.fname)
        dl.load()

        at_c = {}

        for data in dl:
            type = data['Type']
            if not re.match("^$",type):
                continue

            if not srcpt in at_c:
                at_c[srcpt] = {}
                at_c[srcpt]['dstip'] = {}
                at_c[srcpt]['srcip'] = {}

            for dstip in dstip.split():
                if not dstip in at_c[srcpt]['dstip']:
                    at_c[srcpt]['dstip'][dstip] = 0
                at_c[srcpt]['dstip'][dstip] += 1

            for srcip in srcip.split():
                if not srcip in at_c[srcpt]['srcip']:
                    at_c[srcpt]['srcip'][srcip] = 0
                at_c[srcpt]['srcip'][srcip] += 1

        self.at_c = at_c

    def _get_ip2ptr(self, srcip_org):
        if re.match("[0-9\.]+",srcip_org):
            srcip = re.match("[0-9\.]+",srcip_org).group(0)
        else:
            srcip = srcip_org

        # timeout for thread timeout by join()
        self.ip2ptr[srcip_org] = ["timeout","",srcip]

        try:
            self.ip2ptr[srcip_org] = socket.gethostbyaddr(srcip)
        except:
            self.ip2ptr[srcip_org] = ["timeout","",srcip]

    def get_ip2ptr(self):
        # Get All SrcIP List
        tl = []

        for srcpt in self.at_c.keys():
            srcips = self.at_c[srcpt]['srcip']
            for srcip in srcips:
                if not srcip in self.ip2ptr:
                    th = threading.Thread(target=self._get_ip2ptr, args=(srcip,))
                    tl.append(th)
                    th.daemon = True
                    th.start()

        for th in tl:
            th.join(1)

    def show_ip2ptr(self):
        for srcip in self.ip2ptr:
            print("%s: %s"%(srcip,self.ip2ptr[srcip][0]))

    def area_analize(self):
        areas = {}
        for srcip in self.ip2ptr:
            ptr = self.ip2ptr[srcip][0]

            ken = re.match("^.+\.([^\.]+)\.$",ptr)
            if ken:
                area = ken.group(1)
            else:
                ispname = re.match("^.+\.([^\.]+\.[^\.]+\.[^\.]+)$",ptr)
                if ispname:
                    area = ispname.group(1)
                else:
                    area = ptr

            if not area in areas:
                areas[area] = 0

            areas[area] += 1

        self.areas = areas

    def show_areas(self, pref=""):
        for area in self.areas:
            print ("%s%s %d"%(pref, area, self.areas[area]))

if __name__ == "__main__":
    param = sys.argv
    sa = SSDP_Analizer(param[1])
    sa.load()
    sa.get_ip2ptr()
#    sa.show_ip2ptr()
    sa.area_analize()
    sa.show_areas()

