OrientDB Community Edition is available as a binary package for download or as source code on GitHub. The Enterprise Edition is available as a binary package to all our Customers that purchased one of the available Subscriptions. A 45-days Enterprise Edition trial for development purposes is available as well.

OrientDB prerequisites can be found here.

Binary Installation
OrientDB provides a pre-compiled binary package to install the database on your system. Depending on your operating system, this is a tarred or zipped package that contains all the relevant files you need to run OrientDB. For desktop installations, go to OrientDB Downloads and select the package that best suits your system.

On server installations, you can use the wget utility:

$ wget https://s3.us-east-2.amazonaws.com/orientdb3/releases/3.1.0-beta1/orientdb-3.1.0-beta1.tar.gz -O orientdb-community-3.1.0-beta1.tar.gz
Whether you use your web browser or wget, unzip or extract the downloaded file into a directory convenient for your use, (for example, /opt/orientdb/ on Linux). This creates a directory called orientdb-community-3.1.0-beta1 with relevant files and scripts, which you will need to run OrientDB on your system.

Use Docker
If you have Docker installed in your computer, this is the easiest way to run OrientDB. From the command line type:

$ docker run -d --name orientdb -p 2424:2424 -p 2480:2480
   -e ORIENTDB_ROOT_PASSWORD=root orientdb:latest
Where instead of "root", type the root's password you want to use.

More details on how to build your own OrientDB Docker image can be found here

Use Ansible
If you manage your servers through Ansible, you can use the following role : https://galaxy.ansible.com/migibert/orientdb which is highly customizable and allows you to deploy OrientDB as a standalone instance or multiple clusterized instances.

For using it, you can follow these steps :

Install the role

ansible-galaxy install migibert.orientdb
Create an Ansible inventory

Assuming you have one two servers with respective IPs fixed at 192.168.10.5 and 192.168.10.6, using ubuntu user.

[orientdb-servers]
192.168.20.5 ansible_ssh_user=ubuntu
192.168.20.6 ansible_ssh_user=ubuntu
Create an Ansible playbook

In this example, we provision a two node cluster using multicast discovery mode. Please note that this playbook assumes java is already installed on the machine so you should have one step before that install Java 8 on the servers

- hosts: orientdb-servers
  become: yes
  vars:
    orientdb_version: 2.0.5
    orientdb_enable_distributed: true
    orientdb_distributed:
      hazelcast_network_port: 2434
      hazelcast_group: orientdb
      hazelcast_password: orientdb
      multicast_enabled: True
      multicast_group: 235.1.1.1
      multicast_port: 2434
      tcp_enabled: False
      tcp_members: []
    orientdb_users:
      - name: root
        password: root
         tasks:
  - apt:
      name: openjdk-8-jdk
      state: present
  roles:
  - role: orientdb-role
Run the playbook ansible-playbook -i inventory playbook.yml

Source Code Installation
For information on how to install OrientDB from source, please refer to this Section.

Post-installation Tasks
For desktop users installing the binary, OrientDB is now installed and can be run through shell scripts found in the package bin directory of the installation. For servers, there are some additional steps that you need to take in order to manage the database server for OrientDB as a service. The procedure for this varies, depending on your operating system.

Install as Service on Unix, Linux and Mac OS X
Install as Service on Microsoft Windows
Upgrading
When the time comes to upgrade to a newer version of OrientDB, the methods vary depending on how you chose to install it in the first place. If you installed from binary downloads, repeat the download process above and update any symbolic links or shortcuts to point to the new directory.

For systems where OrientDB was built from source, pull down the latest source code and compile from source.

$ git pull origin master
$ mvn clean install
Bear in mind that when you build from source, you can switch branches to build different versions of OrientDB using Git. For example,

$ git checkout 2.2.x
$ mvn clean install
builds the 2.2.x branch, instead of master.

Building a single executable jar with OrientDB
OrientDB for internal components like engines, operators, factories uses Java SPI Service Provider Interface. That means that the jars of OrientDB are shipped with files in META-INF/services that contains the implementation of components. Bear in mind that when building a single executable jar, you have to concatenate the content of files with the same name in different orientdb-*.jar . If you are using Maven Shade Plugin you can use Service Resource Transformer to do that.

Other Resources
To learn more about how to install OrientDB on specific environments, please refer to the guides below:

Install with Docker
Install with Ansible
Install on Linux Ubuntu
Install on JBoss AS
Install on GlassFish
Install on Ubuntu 12.04 VPS (DigitalOcean)
Install on Vagrant

rerequisites
Both editions of OrientDB run on any operating system that implements the Java Virtual machine (JVM), specifically the JDK. Examples of these include:

Linux, all distributions, including ARM (Raspberry Pi, etc.)
Mac OS X
Microsoft Windows
OrientDB requires Java, version 8 or higher, of the JDK.

Note: In OSGi containers, OrientDB uses a ConcurrentLinkedHashMap implementation provided by concurrentlinkedhashmap to create the LRU based cache. This library actively uses the sun.misc package which is usually not exposed as a system package. To overcome this limitation you should add property org.osgi.framework.system.packages.extra with value sun.misc to your list of framework properties.

It may be as simple as passing an argument to the VM starting the platform:

$ java -Dorg.osgi.framework.system.packages.extra=sun.misc

nstallation from Source
In addition to downloading the binary packages, you also have the option of compiling OrientDB from the Community Edition source code, available on GitHub. This process requires that you install Git and Apache Maven on your system.

To compile OrientDB from source code, clone the Community Edition repository, then run Maven (mvn) in the newly created directory:

$ git clone https://github.com/orientechnologies/orientdb
$ git checkout develop
$ cd orientdb
$ mvn clean install
It is possible to skip tests:

$ mvn clean install -DskipTests
The develop branch contains code for the next version of OrientDB. Stable versions are tagged on master branch. For each maintained version OrientDB has its own hotfix branch. As the time of writing this notes, the state of branches is:

develop: work in progress for next 3.0.x release (3.0.x-SNAPSHOT)
2.2.x: hot fix for next 2.2.x stable release (2.2.x-SNAPSHOT)
2.1.x: hot fix for next 2.1.x stable release (2.1.x-SNAPSHOT)
2.0.x: hot fix for next 2.0.x stable release (2.0.x-SNAPSHOT)
last tag on master is 2.2.0
The build process installs all jars in the local maven repository and creates archives under the distribution module inside the target directory. At the time of writing, building from branch 2.1.x gave:

$ls -l distribution/target/
total 199920
    1088 26 Jan 09:57 archive-tmp
     102 26 Jan 09:57 databases
     102 26 Jan 09:57 orientdb-community-2.2.1-SNAPSHOT.dir
48814386 26 Jan 09:57 orientdb-community-2.2.1-SNAPSHOT.tar.gz
53542231 26 Jan 09:58 orientdb-community-2.2.1-SNAPSHOT.zip
$
The directory orientdb-community-2.2.1-SNAPSHOT.dir contains the OrientDB distribution uncompressed. Take a look to Contribute to OrientDB if you want to be involved.

Update Permissions
For Linux, Mac OS X and UNIX-based operating system, you need to change the permissions on some of the files after compiling from source.

$ chmod 755 bin/*.sh
$ chmod -R 777 config
These commands update the execute permissions on files in the config/ directory and shell scripts in bin/, ensuring that you can run the scripts or programs that you've compiled.


nstall as Service on Unix/Linux
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

Other resources
To learn more about how to install OrientDB on specific environment please follow the guide below:

Install on Linux Ubuntu
Install on JBoss AS
Install on GlassFish
Install on Ubuntu 12.04 VPS (DigitalOcean)
Install as service on Unix, Linux and MacOSX
Install as service on Windows
