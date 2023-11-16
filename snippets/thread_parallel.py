#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
##

from concurrent.futures import ThreadPoolExecutor
import subprocess
import time

hosts = ["kevin.qam.suse.de", "sue.qam.suse.de", "adam.qam.suse.de", "alice.qam.suse.de", "antares.qam.suse.de", "crawler.qam.suse.de", "euclid.qam.suse.de", "mira.qam.suse.de", "riguel.qam.suse.de", "riki.qam.suse.de", "rubick.qam.suse.de", "slimer.qam.suse.de", "agnes.qam.suse.de", "bill.qam.suse.de", "clown.qam.suse.de", "roxane.qam.suse.de", "marshmallow.qam.suse.de", "mary.qam.suse.de", "whale-1.qam.suse.de", "whale-10.qam.suse.de", "whale-2.qam.suse.de", "whale-20.qam.suse.de", "whale-26.qam.suse.de", "whale-3.qam.suse.de", "whale-34.qam.suse.de", "whale-4.qam.suse.de", "whale-8.qam.suse.de", "whale-9.qam.suse.de", "whale-25.qam.suse.de", "whale-24.qam.suse.de", "whale-28.qam.suse.de", "whale-30.qam.suse.de", "whale-31.qam.suse.de", "whale-33.qam.suse.de", "whale-5.qam.suse.de", "whale-7.qam.suse.de", "whale-22.qam.suse.de", "whale-27.qam.suse.de", "whale-6.qam.suse.de", "s390vsl012.suse.de", "s390vsl020.suse.de", "s390vsl037.suse.de", "s390vsl048.suse.de", "s390vsl068.suse.de", "s390vsl078.suse.de", "s390vsl136.suse.de", "s390vsl137.suse.de", "s390vsl138.suse.de", "s390vsl134.suse.de", "s390vsl067.suse.de", "s390vsl082.suse.de", "s390vsl130.suse.de", "s390vsl045.suse.de", "s390vsl070.suse.de", "s390vsl073.suse.de", "s390vsl076.suse.de", "s390vsl077.suse.de", "s390vsl083.suse.de", "s390vsl117.suse.de", "s390vsl131.suse.de", "arha.qam.suse.cz", "bojack.qam.suse.cz", "homer.qam.suse.cz", "prague.qam.suse.cz", "tehanu.qam.suse.cz", "tenar.qam.suse.cz", "teradata1.qam.suse.de", "teradata2.qam.suse.de", "fricka.qam.suse.de", "asriel.qam.suse.de", "aziraphale.qam.suse.de", "barbara.qam.suse.de", "belle.qam.suse.de", "deborah.qam.suse.de", "gabriel.qam.suse.de", "geordi.qam.suse.de", "giant.qam.suse.de", "glinda.qam.suse.de", "gorgon.qam.suse.de", "halley.qam.suse.de", "judith.qam.suse.de", "kathryn.qam.suse.de", "naix.qam.suse.de", "omniknight.qam.suse.de", "roke.qam.suse.de", "seven.qam.suse.de", "snowhite.qam.suse.de", "brian.qam.suse.cz", "cascade.qam.suse.cz", "chinook.qam.suse.cz", "chris.qam.suse.cz", "craig.qam.suse.cz", "diane.qam.suse.cz", "goblin.qam.suse.cz", "invoker.qam.suse.cz", "kenny.qam.suse.cz", "lifestealer.qam.suse.cz", "madrid.qam.suse.cz", "metatron.qam.suse.cz", "milan.qam.suse.cz", "orc.qam.suse.cz", "paris.qam.suse.cz", "peter.qam.suse.cz", "tyr.qam.suse.cz", "carolyn.qam.suse.cz", "cartman.qam.suse.cz", "cleveland.qam.suse.cz", "freyr.qam.suse.cz", "glenn.qam.suse.cz", "kyle.qam.suse.cz", "michael.qam.suse.cz", "peanutbutter.qam.suse.cz", "rome.qam.suse.cz", "skeleton.qam.suse.cz", "stewie.qam.suse.cz", "timmy.qam.suse.cz", "troll.qam.suse.cz", "vienna.qam.suse.cz", "marge.qam.suse.cz", "hayley.qam.suse.cz"]

def check_ssh (host):
    cmd = "nc -vzw 5 " + host + " 22"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode

host_status = []
with ThreadPoolExecutor(max_workers=150) as executor:
    #print(executor._max_workers)
    #time.sleep(5)
    ssh_ex = []
    for host in hosts:
        #print(host)
        ssh_ex.append(executor.submit(check_ssh, host))
    
    for host in hosts:
        d = {host: ssh_ex.pop(0).result()}
        host_status.append(d)

print(host_status)


