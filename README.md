This script allows you to benchmark resilver performance of various Zpool / VDEV configurations. 

This is how the script works:
1. Create pool + vdev(s).
2. Write data on pool.
3. Replace arbitrary drive with another one. 
4. Wait for resilver to complete.
5. Grab resilver duration and log to csv file.

Example run-time output. Data is fake.

    root@bunny:~/resilver# ./zfs-benchmark.py zfs-devices.txt 
    2016-01-27 23:29:43,184 - zrb - INFO - pool-mirror-1-2
    2016-01-27 23:30:13,561 - zrb - INFO -  342M resilvered, 69.15% done    342M  69.15% done
    2016-01-27 23:30:33,582 - zrb - INFO - pool-mirror-1-2 Hours: 0 Minutes: 0
    2016-01-27 23:30:43,692 - zrb - INFO - pool-mirror-2-2
    2016-01-27 23:32:13,172 - zrb - INFO - pool-mirror-2-2 Hours: 0 Minutes: 0
    2016-01-27 23:32:23,286 - zrb - INFO - pool-mirror-3-2
    2016-01-27 23:32:29,317 - zrb - INFO - pool-mirror-3-2 Hours: 0 Minutes: 0
    2016-01-27 23:32:39,429 - zrb - INFO - pool-mirror-4-2
    2016-01-27 23:32:45,310 - zrb - INFO - pool-mirror-4-2 Hours: 0 Minutes: 0
    2016-01-27 23:32:55,466 - zrb - INFO - pool-mirror-5-2
    2016-01-27 23:33:01,169 - zrb - INFO - pool-mirror-5-2 Hours: 0 Minutes: 0
    2016-01-27 23:33:11,303 - zrb - INFO - pool-raidz-1-3
    2016-01-27 23:33:18,958 - zrb - INFO - pool-raidz-1-3 Hours: 0 Minutes: 0
    2016-01-27 23:33:29,083 - zrb - INFO - pool-raidz-1-4
    2016-01-27 23:33:55,744 - zrb - INFO - pool-raidz-1-4 Hours: 0 Minutes: 0

The code is not pretty and probably violates some best practices. Work in progress.

Example of csv output: 

    poolname    vdevtype    vdevcount   vdevsize    hours   minutes
    pool-mirror-1-2 mirror  1   2   0   7
    pool-mirror-2-2 mirror  2   2   0   3
    pool-mirror-3-2 mirror  3   2   0   2
    pool-mirror-4-2 mirror  4   2   0   1
    pool-mirror-5-2 mirror  5   2   0   1
    pool-raidz-1-3  raidz   1   3   0   4
    pool-raidz-1-4  raidz   1   4   0   2
    pool-raidz-1-5  raidz   1   5   0   2
    pool-raidz-1-9  raidz   1   9   0   1
    pool-raidz2-1-4 raidz2  1   4   0   4
    pool-raidz2-1-6 raidz2  1   6   0   2
    pool-raidz2-1-10    raidz2  1   10  0   2
    pool-raidz3-1-5 raidz3  1   5   0   4
    pool-raidz3-1-7 raidz3  1   7   0   3
    pool-raidz3-1-11    raidz3  1   11  0   3
