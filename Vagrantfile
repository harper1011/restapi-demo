# -*- mode: ruby -*-
# vi: set ft=ruby :
$script = <<SCRIPT

# Install dependencies
sudo yum -y install epel-release
sudo yum -y update
sudo yum -y install yum-utils python python-pip python-devel rpm-build rpmdevtools redis
sudo yum -y groupinstall "Development Tools"
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install python libraries
sudo pip install --upgrade pip
sudo pip install redis --upgrade
sudo pip install bottle --upgrade
sudo pip install pprint --upgrade
sudo pip install requests --upgrade


# Install and configure docker
sudo yum makecache fast
sudo yum -y install docker-ce
sudo systemctl enable docker
sudo systemctl start docker
sudo groupadd docker
sudo usermod -aG docker $USER

# Start RedisDB
sudo systemctl start redis

SCRIPT

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "boxcutter/centos73"
    config.vm.box_check_update = false

    config.vm.provision "shell", inline: $script

    config.vm.define "Simple-REST-API" do |restapi|
      restapi.vm.hostname = "Simple-REST-API"
    end    
end
