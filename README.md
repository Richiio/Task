To install Answer and get started using it on your system, pull the source code from here using the command

~~~ 
$ git pull origin master 
~~~
 For newer versions of the code, you will just be required to switch branches to build the different versions using Git. For example,

~~~
$ git checkout 2.0
~~~

This will build the 2.0 branch 

## Prerequisites
Answer can run on any operating system 
* Linux, all distributions
* Mac OS X
* Microsoft Windows
* Answer requires Python 3 and higher.

To compile Answer from source code, clone the Task repository, in your command prompt, then start the answer server(which is the server where we are going to be receiving connections).

~~~
$ git clone https://github.com/Richiio/Task
$ cd answer
$ python server.py
~~~

Open another command prompt and run the client server using the following procedures
~~~
$ cd client
$ python client.py
~~~
This would be used for testing purposes to see if we are getting the response from the server that we are meant to be receiving.


## Update Permissions
For Linux, Mac OS X and UNIX-based operating system, you need to change the permissions on some of the files after compiling from source.

~~~
$ chmod 755 bin/*.sh
$ chmod -R 777 config
~~~

These commands update the execute permissions on files in the config/ directory and shell scripts in bin/, ensuring that you can run the scripts or programs that you've compiled.


## Install as Service on Unix/Linux
Following the installation guide above, after cloning the repository to your local system. This doesn't end here, as it does not install Answer at a system-level. There are some additional steps you need to take in order to manage it as a service.

Answer ships with a script, which allows you to manage the server as a system-level daemon. You can find it in the bin/ path of your installation directory, (that is, at $HOME/bin/answer.py

The script supports three parameters:

* start
* stop
* search

Configuring the Script
In order to use the script on your system, you need to edit the file to define two variables: the path to the installation directory and the user you want to run the eoserver.

$ vi $HOME/bin/answer.py

!/bin/sh
answer service script

~~~
chkconfig: 2345 20 80
description: answer init script
processname: answer.py
~~~

### You have to SET the OrientDB installation directory here
ANSWER_DIR="YOUR_ANSWER_INSTALLATION_PATH"
ANSWER_USER="USER_YOU_WANT_ANSWER_RUN_WITH"
Edit the ANSWER_DIR variable to indicate the installation directory. Edit the ANSWER_USER variable to indicate the user you want to run the server.

Installing the Script
Different operating systems and Linux distributions have different procedures when it comes to managing system daemons, as well as the procedure for starting and stopping them during boot up and shutdown. Below are generic guides for init and systemd based unix systems as well Mac OS X. For more information, check the documentation for your particular system.

Installing for init
Many Unix-like operating systems such as FreeBSD, most older distributions of Linux, as well as current releases of Debian, Ubuntu and their derivatives use variations on SysV-style init for these processes. These are typically the systems that manage such processes using the service command.

To install HOME as a service on an init-based unix or Linux system, copy the modified orientdb.sh file from $ORIENTDB_HOME/bin into /etc/init.d/:

~~~
cp $ORIENTDB_HOME/bin/orientdb.sh /etc/init.d/orientdb
Once this is done, you can start and stop OrientDB using the service command:
~~~

# service orientdb start
Starting OrientDB server daemon...
Installing for systemd
Most newer releases of Linux, especially among the RPM-based distributions like Red Hat, Fedora, and CentOS, as well as future releases of Debian and Ubuntu use systemd for these processes. These are the systems that manage such processes using the systemctl command.

The OrientDB's package contains a service descriptor file for systemd based distros. The orientdb.service is placed in the bin directory. To install OrientDB copy the orientdb.service to/etc/systemd/system directory (check this, may depend on distro). Edit the file:

# vi /etc/systemd/system/orientdb.service

~~~
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
~~~

Set the right user and group. You may want to use the absolute path instead of the environment variable $ORIENTDB_HOME. Once this file is saved, you can start and stop the OrientDB server using the systemctl command:

### systemctl start orientdb.service
Additionally, with the orientdb.service file saved, you can set systemd to start the database server automatically during boot by issuing the enable command:

### systemctl enable orientdb.service
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

The installation process setups a default server's root user password that must be changed. The orientdb-server-config.xml file is installed in /usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/config/. Open the file and remove the "root" user entry. Remove the tag true at the end of the file. Start the server on interactive console:

/usr/local/Cellar/orientdb/<ORIENTDB_VERSION>/libexec/bin/server.sh
The script asks for a new password for the server's root user.

