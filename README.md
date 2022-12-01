Following the installation guide above, whether you choose to download binaries or build from source, does not install OrientDB at a system-level. There are a few additional steps you need to take in order to manage the database system as a service.

OrientDB ships with a script, which allows you to manage the database server as a system-level daemon. You can find it in the bin/ path of your installation directory, (that is, at $ORIENTDB_HOME/bin/orientdb.sh.

The script supports three parameters:

start
stop
status
Configuring the Script
In order to use the script on your system, you need to edit the file to define two variables: the path to the installation directory and the user you want to run the database server.

$ vi $ORIENTDB_HOME/bin/orientdb.sh

#!/bin/sh
# OrientDB service script
#
# Copyright (c) Orient Technologies LTD (http://www.orientechnologies.com)

# chkconfig: 2345 20 80
# description: OrientDb init script
# processname: orientdb.sh

# You have to SET the OrientDB installation directory here
ORIENTDB_DIR="YOUR_ORIENTDB_INSTALLATION_PATH"
ORIENTDB_USER="USER_YOU_WANT_ORIENTDB_RUN_WITH"
Edit the ORIENTDB_DIR variable to indicate the installation directory. Edit the ORIENTDB_USER variable to indicate the user you want to run the database server, (for instance, orientdb).

Installing the Script
Different operating systems and Linux distributions have different procedures when it comes to managing system daemons, as well as the procedure for starting and stopping them during boot up and shutdown. Below are generic guides for init and systemd based unix systems as well Mac OS X. For more information, check the documentation for your particular system.

Installing for init
Many Unix-like operating systems such as FreeBSD, most older distributions of Linux, as well as current releases of Debian, Ubuntu and their derivatives use variations on SysV-style init for these processes. These are typically the systems that manage such processes using the service command.

To install OrientDB as a service on an init-based unix or Linux system, copy the modified orientdb.sh file from $ORIENTDB_HOME/bin into /etc/init.d/:

# cp $ORIENTDB_HOME/bin/orientdb.sh /etc/init.d/orientdb
Once this is done, you can start and stop OrientDB using the service command:

# service orientdb start
Starting OrientDB server daemon...
Installing for systemd
Most newer releases of Linux, especially among the RPM-based distributions like Red Hat, Fedora, and CentOS, as well as future releases of Debian and Ubuntu use systemd for these processes. These are the systems that manage such processes using the systemctl command.

The OrientDB's package contains a service descriptor file for systemd based distros. The orientdb.service is placed in the bin directory. To install OrientDB copy the orientdb.service to/etc/systemd/system directory (check this, may depend on distro). Edit the file:

# vi /etc/systemd/system/orientdb.service

#
# Copyright (c) OrientDB LTD (http://http://orientdb.com/)
#

[Unit]
Description=OrientDB Server
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=ORIENTDB_USER
Group=ORIENTDB_GROUP
ExecStart=$ORIENTDB_HOME/bin/server.sh

Set the right user and group. You may want to use the absolute path instead of the environment variable $ORIENTDB_HOME. Once this file is saved, you can start and stop the OrientDB server using the systemctl command:

# systemctl start orientdb.service
Additionally, with the orientdb.service file saved, you can set systemd to start the database server automatically during boot by issuing the enable command:

# systemctl enable orientdb.service
Synchronizing state of orientdb.service with SysV init with /usr/lib/systemd/systemd-sysv-install...
Executing /usr/lib/systemd/systemd-sysv-install enable orientdb
Created symlink from /etc/systemd/system/multi-user.target.wants/orientdb.service to /etc/systemd/system/orientdb.service.
Installing for Mac OS X
Manual install
For Mac OS X:

follow the steps described above, in the Configuring the Script section
create an alias to the OrientDB system daemon script and the console.
$ alias orientdb-server=/path/to/$ORIENTDB_HOME/bin/orientdb.sh
$ alias orientdb-console=/path/to/$ORIENTDB_HOME/bin/console.sh
You can now start the OrientDB database server using the following command:

$ orientdb-server start
Once the database starts, it is accessible through the console script.

$ orientdb-console

OrientDB console v.1.6 www.orientechnologies.com
Type 'HELP' to display all the commands supported.

orientdb>
Brew
OrientDB is available through brew.

$ brew install orientdb
The installation process gives an output similar to the following one:

...
==> Downloading https://orientdb.com/download.php?file=orientdb-community-<ORIENTDB_VERSION>.tar.gz
==> /usr/bin/nohup  /usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/bin/server.sh &
==> /usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/bin/shutdown.sh
==> OrientDB installed, server's root user password is 'changeme'
==> Please, follow the instruction on the link below to reset it
==> http://orientdb.com/docs/2.2/Server-Security.html#restoring-the-servers-user-root
...
The installation process setups a default server's root user password that must be changed. The orientdb-server-config.xml file is installed in /usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/config/. Open the file and remove the "root" user entry. Remove the tag true at the end of the file. Start the server on interactive console:

/usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/bin/server.sh
The script asks for a new password for the database's root user.
