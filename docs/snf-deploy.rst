.. _snf-deploy:

snf-deploy tool
^^^^^^^^^^^^^^^

The `snf-deploy` tool allows you to automatically deploy Synnefo.
You can use `snf-deploy` to deploy Synnefo, in two ways:

1. Create a virtual cluster on your local machine and then deploy on that cluster.
2. Deploy on a pre-existent cluster of physical nodes running Debian Wheezy.

Currently, `snf-deploy` is mostly useful for testing/demo installations and is
not recommended for production environment Synnefo deployments. If you want to
deploy Synnefo in production, please read first the :ref:`Admin's installation
guide <quick-install-admin-guide>` and then the :ref:`Admin's guide
<admin-guide>`.

If you use `snf-deploy` you will setup an up-and-running Synnefo installation,
but the end-to-end functionality will depend on your underlying infrastracture
(e.g.  is nested virtualization enabled in your PC, is the router properly
configured, do nodes have fully qualified domain names, etc.). In any way, it
will enable you to get a grasp of the Web UI/API and base funtionality of
Synnefo and also provide a proper configuration that you can afterwards consult
while reading the Admin guides to set up a production environment that will
scale up and use all available features (e.g. RADOS, Archipelago, etc).

`snf-deploy` is a debian package that should be installed locally and allows
you to install Synnefo locally, or on remote nodes,  or spawn a cluster of VMs
on your local machine using KVM and then install Synnefo on this cluster. To
this end, here we will break down our description into three sections:

a. :ref:`snf-deploy configuration <conf>`
b. :ref:`Creating a virtual cluster <vcluster>` (needed for (1))
c. :ref:`Synnefo deployment <inst>` (either on virtual nodes created on section b,
   or on remote physical nodes)

If you go for (1) you will need to walk through all the sections. If you go for
(2), you should skip section `(b) <vcluster>`, since you only need sections
`(a) <conf>` and `(c) <inst>`.

Before getting any further we should mention the roles that `snf-deploy` refers
to. The Synnefo roles are described in detail :ref:`here
<physical-node-roles>`. Those nodes consist of certain components.
Note that multiple roles can co-exist in the same node
(virtual or physical).

Currently, `snf-deploy` defines the following roles:

* ns: bind server (DNS)
* db: postgresql server (database)
* mq: rabbitmq server (message queue)
* nfs: nfs server
* astakos: identity service
* pithos: storage service
* cyclades: compute service
* cms: cms service
* stats: stats service
* ganeti: ganeti node
* master: master node


The previous roles are combinations of the following software components:

* HW: IP and internet access
* SSH: ssh keys and config
* DDNS: ddns keys and ddns client config
* NS: nameserver with ddns config
* DNS: resolver config
* APT: apt sources config
* DB: database server with postgresql
* MQ: message queue server with rabbitmq
* NFS: nfs server
* Mount: nfs mount point
* Apache: web server with Apache
* Gunicorn: gunicorn server
* Common: synnefo common
* WEB: synnefo webclient
* Astakos: astakos webapp
* Pithos: pithos webapp
* Cyclades: cyclades webapp
* CMS: cms webapp
* VNC: vnc authentication proxy
* Collectd: collectd config
* Stats: stats webapp
* Kamaki: kamaki client
* Burnin: qa software
* Ganeti: ganeti node
* Master: ganeti master node
* Image: synnefo image os provider
* Network: synnefo networking scripts
* GTools: synnefo tools for ganeti
* GanetiCollectd: collectd config for ganeti nodes

Each component defines the following things:

* commands to check prereqs
* commands to prepare installation
* list of packages to install
* specific configuration files (templates)
* restart/reload commands
* initialization commands
* test commands

All a components needs is the node info that it gets installed to and the
snf-deploy configuration environment (available after parsing conf files).

.. _conf:

Configuration (a)
=================

All configuration of `snf-deploy` happens by editting the following files under
``/etc/snf-deploy``:

``nodes.conf``
--------------

This file reflects the hardware infrastucture on which Synnefo is going to be
deployed and is the first to be set before running `snf-deploy`.

Defines the nodes' hostnames and their IPs. Currently `snf-deploy` expects all
nodes to reside under the same domain. Since Synnefo requires FQDNs to operate,
a nameserver is going to be automatically setup in the cluster by `snf-deploy`
and all nodes with use this node for resolver.

Also, defines the nodes' authentication credentials (username, password).
Furthermore, whether nodes have an extra disk (used for LVM/DRBD storage in
Ganeti backends) or not. The VM container nodes should have three separate
network interfaces (either physical or vlans) each in the same collision
domain; one for the node's public network, one for VMs' public network and one
for VMs' private networks. In order to support the most common case, a router
is setup on the VMs' public interface and does NAT (hoping the node has itself
internet access).

The nodes defined in this file can reflect a number of physical nodes, on which
you will deploy Synnefo (option (2)), or a number of virtual nodes which will
get created by `snf-deploy` using KVM (option (1)), before deploying Synnefo.
As we will see in the next sections, one should first set up this file and then
tell `snf-deploy` whether the nodes on this file should be created, or treated
as pre-existing.

In case you deploy all-in-one you can install `snf-deploy` package in the
target node and use `--autoconf` option. By that you must change only
the passwords section and everything else will be automatically configured.

An example ``nodes.conf`` file looks like this:

FIXME: example file here

``synnefo.conf``
----------------

This file reflects the way Synnefo will be deployed on the nodes defined at
``nodes.conf``.

The important section here is the roles. In this file we assing each of the
roles described in the :ref:`introduction <snf-deploy>` to a specific node. The
node is one of the nodes defined at ``nodes.conf``. Note that we refer to nodes
with their ID (node1, node2, etc).

Here we also define all credentials related to users needed by the various
Synnefo services (database, RAPI, RabbitMQ) and the credentials of a test
end-user (`snf-deploy` simulates a user signing up).

Furthermore, define the Pithos shared directory which will hold all the Pithos
related data (maps and blocks).

Finally, define the name of the bridge interfaces controlled by Synnefo, and a
testing Image to register after everything is up and running.

An example ``setup.conf`` file (based on the previous ``nodes.conf`` example)
looks like this:

FIXME: example file here

``ganeti.conf``
---------------

This file reflects the way Ganeti clusters will be deployed on the nodes
defined at ``nodes.conf``.

Here we include all info with regard to Ganeti backends. That is: the master
node, its floating IP, the rest of the cluster nodes (if any) the volume group
name (in case of LVM support) and the VMs' public network associated to it.

FIXME: example file here

``deploy.conf``
---------------

This file customizes `snf-deploy` itself.

It defines some needed directories and also includes options that have to do
with the source of the packages to be deployed. Specifically, whether to deploy
using local packages found under a local directory or deploy using an apt
repository. If deploying from local packages, there is also an option to first
download the packages from a custom URL and save them under the local directory
for later use.

FIXME: example file here

``vcluster.conf``
-----------------

This file defines options that are relevant to the virtual cluster creation, if
one chooses to create one.

There is an option to define the URL of the Image that will be used as the host
OS for the VMs of the virtual cluster. Also, options for defining an LVM space
or a plain file to be used as a second disk. Finally, networking options to
define where to bridge the virtual cluster.


.. _vcluster:

Virtual Cluster Creation (b)
============================

As stated in the introduction, `snf-deploy` gives you the ability to create a
local virtual cluster using KVM and then deploy Synnefo on top of this cluster.
The number of cluster nodes is arbitrary and is defined in ``nodes.conf``.

This section describes the creation of the virtual cluster, on which Synnefo
will be deployed in the :ref:`next section <inst>`. If you want to deploy
Synnefo on existing physical nodes, you should skip this section.

The first thing you need to deploy a virtual cluster, is a Debian Base image,
which will be used to spawn the VMs.

FIXME: Find a way to provide this image.

The virtual cluster can be created by running:

.. code-block:: console

   snf-deploy vcluster

This will download the image from the URL defined at ``squeeze_image_url``
(Pithos by default) and save it locally under ``/var/lib/snf-deploy/images``.

TODO: mention related options: --img-dir, --extra-disk, --lvg, --os

Afterwards it will add a bridge (defined with the ``bridge`` option inside
``vcluster.conf``), iptables to allow traffic from/to the cluster, and enable
forwarding and NAT for the selected network subnet (defined inside
``nodes.conf`` in the ``subnet`` option).

To complete the preparation, you need a DHCP server that will provide the
selected hostnames and IPs to the cluster (defined under ``[ips]`` in
``nodes.conf``).

It will launch a dnsmasq instance, acting only as DHCP server and listening
only on the cluster's bridge.

Finally it will launch all the needed KVM virtual machines, snapshotting the
image we fetched before. Their taps will be connected with the already created
bridge and their primary interface will get the given address.

Now that we have the nodes ready, we can move on and deploy Synnefo on them.


.. _inst:

Synnefo Installation (c)
========================

At this point you should have an up-and-running cluster, either virtual
(created in the :ref:`previous section <vcluster>` on your local machine) or
physical on remote nodes. The cluster should also have valid hostnames and IPs.
And all its nodes should be defined in ``nodes.conf``.

You should also have set up ``synnefo.conf`` to reflect which Synnefo component
will reside in which node.

Node Requirements
-----------------

 - OS: Debian Wheezy
 - authentication: `root` user with corresponding for each node password
 - primary network interface: `eth0`
 - spare network interfaces: `eth1`, `eth2` (or vlans on `eth0`)

In case you have created a virtual cluster as described in the :ref:`section
(b) <vcluster>`, the above requirements are already taken care of. In case of a
physical cluster, you need to set them up manually by yourself, before
proceeding with the Synnefo installation.


Synnefo deployment
------------------

To install the Synnefo stack on the existing cluster run:

.. code-block:: console

   snf-deploy all -vvv

This might take a while.

If this finishes without errors, check for successful installation by visiting
from your local machine (make sure you have already setup your local
``resolv.conf`` to point at the cluster's DNS):

| https://accounts.synnefo.live/astakos/ui/

and login with:

| username: user@synnefo.org password: 12345

or the ``user_name`` and ``user_passwd`` defined in your ``synnefo.conf``.
Take a small tour checking out Pithos and the rest of the Web UI. You can
upload a sample file on Pithos to see that Pithos is working. To test
everything went as expected, visit from your local machine:

.. code-block:: console

    https://cyclades.synnefo.live/cyclades/ui/

and try to create a VM. Also create a Private Network and try to connect it. If
everything works, you have setup Synnefo successfully. Enjoy!


Adding another Ganeti Backend
-----------------------------

From version 0.12, Synnefo supports multiple Ganeti backends.
`snf-deploy` defines them in ``ganeti.conf``.

After adding another section in ``ganeti.conf``, run:

.. code-block:: console

   snf-deploy backend --cluster-name ganeti2 -vvv


snf-deploy for Ganeti
=====================

`snf-deploy` can be used to deploy a Ganeti cluster on pre-existing nodes
by issuing:

.. code-block:: console

   snf-deploy ganeti --cluster-name ganeti3 -vvv


snf-deploy as a DevTool
=======================

For developers, a single node setup is highly recommended and `snf-deploy` is a
very helpful tool. `snf-deploy` also setting up components using packages that
are locally generated. For this to work please add all related \*.deb files in
packages directory (see ``deploy.conf``) and set the ``use_local_packages``
option to ``True``. Then run:

.. code-block:: console

   snf-deploy run <action1> [<action2>..]


to execute predefined actions or:

.. code-block:: console

   snf-deploy run setup --node nodeX \
        --role ROLE | --component COMPONENT --method METHOD

to setup a synnefo role on a target node or run a specific component's method.

For instance, to add another node to an existing ganeti backend run:

.. code-block:: console

   snf-deploy run setup --node5 --role ganeti --cluster-name ganeti3

`snf-deploy` keeps track of installed components per node in
``/etc/snf-deploy/status.conf``. If a deployment command fails, the developer
can make the required fix and then re-run the same command; `snf-deploy` will
not re-install components that have been already setup and their status
is ``ok``.
