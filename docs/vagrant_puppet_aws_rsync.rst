Vagrant AWS Puppet Rsync
======


While deploying from vagrant to AWS using vagrant-aws, 
you may run into an error if you are sharing folders. To share folders on AWS, you would use rsync.

If rsync is not installed on your base AMI, you may run into an issue where you are unable to share your folders and your box will not provision.

Before initialiting puppet, you will want to use a script to install rsync

Here is my vagrant file + custom init script to resolve this issue

.. code-block:: ruby

    # Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
    VAGRANTFILE_API_VERSION = "2"

    Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|  
      config.vm.box = "dummy"
      config.ssh.pty = true
      config.vm.define :awsinstance do |awsi|
        # setup ami, aws
        awsi.vm.provider :aws do |aws, override|
            aws.keypair_name = "YOURKEYPAIR"
            aws.access_key_id = ""
            aws.secret_access_key = ""
            aws.region = "us-east-1"
            # debian wheezy 7.6
            aws.ami = "ami-c4ab67ac"
            override.ssh.private_key_path = "YOURPRIVATEKEY"
            override.ssh.username = "USERNAME"
        end
        # setup puppet
        awsi.vm.hostname = "myvm"
        awsi.vm.provision :shell, :path => "shell/init.sh"
        awsi.vm.provision :puppet do |awspuppet|
            awspuppet.manifest_file = "nodes.pp"
            awspuppet.manifests_path = "/myapp/manifests/manifests"
            awspuppet.module_path = "/myapp/manifests/modules"
        end
        # mount folders
        awsi.vm.synced_folder "/myapp/stuff", "/myapp/stuff",
                              owner: "admin",
                              group: "root",
                              :mount_options => ['dmode=775','fmode=775'], type: "rsync"
      end
      config.ssh.forward_agent = false
    end

The shell/init.sh script (which is ran before puppet modules are initialized):

.. code-block:: bash

    #!/bin/sh
    $(which rsync > /dev/null 2>&1)
    FOUND_RSYNC=$?  
    if [ "$FOUND_RSYNC" -ne '0' ]; then  
        echo 'Attempting to install rsync'
        $(which apt-get > /dev/null 2>&1)
        FOUND_APT=$?
        $(which yum > /dev/null 2>&1)
        FOUND_YUM=$?

        if [ "${FOUND_YUM}" -eq '0' ]; then
            yum -q -y makecache
            yum -q -y install rsync
            echo 'rsync installed.'
            yum -q -y install puppet
            echo 'puppet installed.'
        elif [ "${FOUND_APT}" -eq '0' ]; then
            apt-get -q -y update
            apt-get -q -y install rsync
            echo 'rsync installed.'
            apt-get -q -y install puppet
            echo 'puppet installed.'
        else
            echo 'No package installer available'
        fi
    fi  
    # Set the first portion of this to match the node defined in your manifest
    # example node of crunch should be crunch.X
    hostname myvm.va.localdomain
