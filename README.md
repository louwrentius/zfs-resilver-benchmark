This script allows you to benchmark resilver performance of various Zpool / VDEV configurations. 

This is how the script works:
1. Create pool + vdev(s).
2. Write data on pool.
3. Replace arbitrary drive with another one. 
4. Wait for resilver to complete.
5. Grab resilver duration and log to csv file.

The script takes one argument that specifies the file name containing the names of the hard drive devices, one per line.
An example file called 'zfs-devices.txt' is added to this repro.

When you put the csv data in Excel or something similar you get results like:

![image][image]

[image]:http://louwrentius.com/static/images/zfs-resilver-benchmark01.png
