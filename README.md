This script allows you to benchmark resilver performance of various Zpool / VDEV configurations. 

This is how the script works:

1. Create pool + vdev(s).
2. Write data on pool.
3. Replace arbitrary drive with another one. 
4. Wait for resilver to complete.
5. Grab resilver duration and log to csv file.

The script takes one argument that specifies the file name containing the names of the hard drive devices, one per line.
An example file called 'zfs-devices.txt' is added to this repro.

You need to edit the script and alter the 'main' function to ajust for the types of test you want to run.
You can comment out the VDEV types (Mirror/RAID-Z) you don't want to run.

    bench.poolname = 'pool'
    bench.vdev['mirror'] = [2]
    bench.vdev['mirrorvdevs'] = [1]
    bench.vdev['mirrorvdevs'] = [1,2,3,4,5]
    bench.vdev['raidz'] = [3,4,5,9]
    bench.vdev['raidzvdevs'] = [1]
    bench.vdev['raidz2'] = [10]
    bench.vdev['raidz2vdevs'] = [1]
    #bench.vdev['raidz3'] = [5,7,11]
    #bench.vdev['raidz3vdevs'] = [1]
    bench.data = 50 # % of pool size


When you put the csv data in Excel or something similar you get results like:

![image][image]

[image]:http://louwrentius.com/static/images/zfs-resilver-benchmark01.png
