Useful Sysadmin Commands
======

A collection of helpful Linux / Freebsd commands I find helpful for day to day use

Finding files and executing actions on them
------------------

Find and delete files with filename length of 5::

    find . -type f -name '?????' -exec rm -f {} \;

Remove all data from file without deleting file::

    truncate -s0 access.log

List all file and directory disk space usage sorted by 10 largest directories::

    sudo du -cks * | sort -rn | head

Listing processes and process system usage
------------------

List memory usage by category of process::

    ps aux | awk '{print $4"\t"$11}' | sort | uniq -c | awk '{print $2" "$1" "$3}' | sort -nr 

List memcache objects::

    ngrep -W none -T -d any "^(get|set|delete|END|STORED|VALUE|DELETED)" port 11211 | awk '{print $1 " " $2}'

SSH Commands
------------------

Forward custom port (local requests to MySQL in this example) to a remote host::

    ssh -fND 3306 username@bestwebsiteintheworld.com

Troubleshooting Network Traffic
------------------
List open ports::

    netstat -tulpn
    nmap -v -sU localhost

Capture http headers with tcpdump::

    tcpdump -s 1024 -C 1024000 -w /tmp/httpcapture dst port 80

Check for connections to a database not closing (left in TIME_WAIT status)::

    netstat -an | grep TIME_WAIT

Capture packets for a particular Destination IP and Port::

    tcpdump -w packet_capture_results.pcap -i eth0 dst 10.0.1.8 and port 22

Capture all packets except those that match packet type filter::

    tcpdump -i eth0 not arp and not rarp

Capture UDP packets::

    tcpdump -i eth0 udp

Show list of banned ips::

    sudo iptables -L -n | awk '$1=="REJECT" && $4!="0.0.0.0/0" {print $4}'

Show list of all banned ips with jails::

    sh -c "fail2ban-client status | sed -n 's/,//g;s/.*Jail list://p' | xargs -n1 fail2ban-client status"

Tar Commands
------------------

Tar a directory and encrypt it in one line::

    tar cvzf - example_dir | openssl des3 -salt -k secretkey | dd of=encrypted_example_dir

To decrypt::

    dd if=encrypted_example_dir | openssl des3 -d -k secretkey | tar xvzf - 
