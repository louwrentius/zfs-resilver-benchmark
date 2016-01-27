#!/usr/bin/python

import sys
import os
import csv
import subprocess
import time
import re
import random
import copy
import logging

filename = sys.argv[1]

class zpool:

    def __init__(self, properties, devices, logger):
        self.used_zpooldevices = []
        self.zpooldevices = copy.deepcopy(devices)
        self.poolname = properties['poolname']
        self.vdevtype = properties['vdevtype']
        self.vdevsize = properties['vdevsize']
        self.vdevcount = properties['vdevcount']
	self.logger = logger

    def get_disk_line(self):
        line = ""
        for disk in range(self.vdevsize):
            device = self.zpooldevices.pop()
            self.used_zpooldevices.append(device)
            line += " " + device
        return line

    def create_vdev(self):
        line = " " + self.vdevtype
        dev = self.get_disk_line()
        line += dev
        return line

    def run_cmd(self, command):
        p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True)
        rawdata = p.communicate()
        returncode = p.returncode
        return rawdata

    def create(self):
        devices = ""
        for vdev in range(self.vdevcount):
            devices += self.create_vdev()
        command = "zpool create " + self.poolname + " " + devices + " -f" 
        output = self.run_cmd(command)
        while output[1]:
            output = self.run_cmd(command)
            time.sleep(20)

    def destroy(self):
        command = "zpool destroy -f " + self.poolname 
        output = self.run_cmd(command)

    def status(self):
        command = "zpool status " + self.poolname 
        output = self.run_cmd(command)
        pooldata = output[0]
        return pooldata

    def get_resilver_performance(self):
        output = self.status()
        pattern = "scan: resilvered"
        regex = re.compile('(\d*)h(\d*)m')
        match = regex.search(output)
        data = {}
        if match:
            data['hours'] = match.group(1)
            data['minutes'] = match.group(2)
            return data
        else:
            time.sleep(20)
            self.get_resilver_performance()

    def write_data(self, size):
        command = "dd if=/dev/zero of=/" + self.poolname + "/test.bin bs=1M count=" + str(size) + " conv=sync"
        output = self.run_cmd(command)
        return output

    def resilver_in_progress(self):
        data = self.status()
        pattern = "(action: Wait for the resilver to complete.)"
        regex = re.compile(pattern)
        match = regex.search(data)
        if match:
            return True
        else:
            return False

    def resilver_status(self):
        data = self.status()
        pattern = "(.*)resilvered,(.*)"
        regex = re.compile(pattern)
        match = regex.search(data)
        result = str(match.group(0)) + str(match.group(1)) + str(match.group(2))
        return result 

    def wait_for_resilver(self):
        while self.resilver_in_progress():
            self.logger.info(self.resilver_status())
            time.sleep(20)

    def replace_drive(self):
        replacement = self.zpooldevices.pop()
        num_devices = len(self.used_zpooldevices)
        rand = random.randrange(0, num_devices)
        tobereplaced = self.used_zpooldevices[rand]
        command = "zpool replace " + self.poolname + " " + str(tobereplaced) + " " + str(replacement) + " -f"
        output = self.run_cmd(command)
	try:
	        self.logger.debug(output)
	except ValueError:
		time.sleep(10)
		self.replace_drive()
	
        self.used_zpooldevices.append(replacement)
        return output


class benchmark:

    def __init__(self, filename):
        self.devices = self.get_devices(filename)
        self.poolname = ""
        self.vdev = {}
        self.logger = logging.getLogger('zrb')
        self.logger.setLevel(logging.INFO)
        self.benchmarkresults = []
        self.ch = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)


    def benchmark_pool(self, properties):
        pool = zpool(properties, self.devices, self.logger)
        self.logger.info(properties['poolname'])
        pool.create()
        pool.write_data(100000)
        pool.replace_drive()
        pool.wait_for_resilver()

        data = pool.get_resilver_performance()
        mydict = {}
        mydict = copy.deepcopy(properties)
        mydict['hours'] = data['hours']
        mydict['minutes'] = data['minutes']
        self.benchmarkresults.append(mydict)
        self.write_csv()
        self.logger.info( str(properties['poolname']) + " Hours: " + str(data['hours']) + " Minutes: " + str(data['minutes']))
        pool.destroy()
        time.sleep(10)

    def write_csv(self):
        filename = "benchmark-output.csv"
        with open(filename, 'w') as csvfile:
            fieldnames = ['poolname','vdevtype','vdevcount','vdevsize','hours','minutes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.benchmarkresults:
                writer.writerow(row)



    def bench(self):
        vdevtypes = ['mirror', 'raidz', 'raidz2', 'raidz3']

        properties = {}

        for vdevtype in vdevtypes:
            try:
                if self.vdev[vdevtype]:
                    vd = str(vdevtype) + "vdevs"
                    for numvdevs in self.vdev[vd]:
                        for d in self.vdev[vdevtype]:
                            properties['poolname'] = self.poolname + "-" + str(vdevtype) + "-" + str(numvdevs) + "-" + str(d)
                            properties['vdevtype'] = vdevtype
                            properties['vdevsize'] = d
                            properties['vdevcount'] = numvdevs

                            self.benchmark_pool(properties)
            except KeyError:
                pass

    def get_devices(self, filename):
        devices = []
        with open(filename,'r') as f:
            for row in f.read().splitlines():
                devices.append(row)
        return devices
        
def main():
    bench = benchmark(filename)
    bench.poolname = 'pool'
    bench.vdev['mirror'] = [2]
    #bench.vdev['mirrorvdevs'] = [1]
    bench.vdev['mirrorvdevs'] = [1,2,3,4,5]
    bench.vdev['raidz'] = [3,4,5,9]
    bench.vdev['raidzvdevs'] = [1]
    bench.vdev['raidz2'] = [4,6,10]
    bench.vdev['raidz2vdevs'] = [1]
    bench.vdev['raidz3'] = [5,7,11]
    bench.vdev['raidz3vdevs'] = [1]
    bench.bench()

if __name__ == "__main__":
    main()

