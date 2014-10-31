from ssdpchecker import SSDP_Analizer
import sys
import re

if __name__ == "__main__":
    param = sys.argv
    date = re.match("^.*list_([0-9]+).*$",param[1]).group(1)
    sa = SSDP_Analizer(param[1])
    sa.load("0")
    sa.get_ip2ptr()
#    sa.show_ip2ptr()
    sa.area_analize()
    sa.show_areas(date+" ")

