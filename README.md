Simple RESTful Server
====
Simple RESTFul Server for demo purpose:

The RESTful API need to be accessed via following URL:
http://$SERVER_IP:3000/api/v1
As for demo purpose, there is only v1 avaliable. All the undefined URL access will HTTP Status Code with 404

There are some examples:
* Listing of cached items
    * URL: "http://$SERVER_IP:3000/api/v1"
    * REQUEST_METHOD: "GET"
* Viewing a single item
    * URL: "http://$SERVER_IP:3000/api/v1/$index"
    * REQUEST_METHOD: "GET"
* Creating an item
    * URL: "http://$SERVER_IP:3000/api/v1/$index"
    * REQUEST_METHOD: "POST"
* Deleting an item
    * URL: "http://$SERVER_IP:3000/api/v1/$index"
    * REQUEST_METHOD: "DELETE"
* Updating an item, for instance a new location
    * URL: "http://$SERVER_IP:3000/api/v1/$index"
    * REQUEST_METHOD: "PUT"

--------------------------------------------------------------------------------------------------
There are two ways to test it:

* Build this project into rpm package and install it, then access via ***localhost*** as host IP.

    * Step by step:
        * Use provided Vagrantfile to init a CentOS VM
        
            ```
            E:\code\playground\restapi-demo>vagrant up
            ```
        * Log into Vagrant enviroment and then move to this project folder and make sure all project files can be seen from this folder
        
            ```
            E:\code\playground\restapi-demo>vagrant ssh
            Last login: Wed Jun 21 12:24:55 2017 from 10.0.2.2
            ----------------------------------------------------------------
              CentOS 7.3.1611                             built 2016-12-15
            ----------------------------------------------------------------
            [vagrant@Simple-REST-API ~]$ cd /vagrant/
            [vagrant@Simple-REST-API vagrant]$ ls
            Dockerfile  Makefile  README.md  scripts  SOURCES  SPECS  testing.log  Vagrantfile
            ```
        * Compile project into RPM package
        
            ```
            [vagrant@Simple-REST-API vagrant]$ make clean rpm
            ```
        * Install rpm file then start ***restapi*** service and make sure ***restapi*** service working properly
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo rpm -ivh --replacepkgs simple-restapi-server-*.rpm --force
            [vagrant@Simple-REST-API vagrant]$ sudo systemctl start restapi
            [vagrant@Simple-REST-API vagrant]$ sudo systemctl status restapi
            ● restapi.service - Simple RESTful server
               Loaded: loaded (/usr/lib/systemd/system/restapi.service; disabled; vendor preset: disabled)
               Active: active (running) since Wed 2017-06-21 12:30:25 UTC; 15s ago
             Main PID: 4341 (python)
               Memory: 9.2M
               CGroup: /system.slice/restapi.service
                       └─4341 python /opt/script/restapi/simple_rest_server.py localhost 3000

            Jun 21 12:30:25 Simple-REST-API systemd[1]: Started Simple RESTful server.
            Jun 21 12:30:25 Simple-REST-API systemd[1]: Starting Simple RESTful server...
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: 2017-06-21 12:30:25,585 simple_rest_server:25 [INFO] Connect to RedisDB successfully. Use RedisDB for storing data.
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: 2017-06-21 12:30:25,589 simple_rest_server:177[INFO] Override bind IP and port to: localhost:3000
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: 2017-06-21 12:30:25,589 simple_rest_server:181[INFO] Starting server with localhost:3000
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: Bottle v0.12.13 server starting up (using WSGIRefServer())...
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: Listening on http://localhost:3000/
            Jun 21 12:30:25 Simple-REST-API simple_rest_server.py[4341]: Hit Ctrl-C to quit.
            ```
        * Send your own REST query to *http://localhost:3000/api/v1* or run Unit Testcase with following command to see whether the simple rest server is working properly
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo python SOURCES/test_rest_server.py
            .
            ----------------------------------------------------------------------
            Ran 1 test in 0.176s

            OK
            ```

    * All in one script:
        * Use provided Vagrantfile to init a CentOS VM.
        * Log into Vagrant enviroment and then move to this project folder and make sure all project files can be seen from this folder
        * Execute command in order to make auto setup the same as *step by step* section
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo python scripts/all-in-one.py
            ```
        * Send your own REST query to *http://localhost:3000/api/v1* or run Unit Testcase with following command to see whether the simple rest server is working
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo python SOURCES/test_rest_server.py
            .
            ----------------------------------------------------------------------
            Ran 1 test in 0.176s

            OK
            ```

* Run ***Simple-REST-API*** in docker containers, then access via its container's host IP.

    * Step by step
        * Use provided Vagrantfile to init a CentOS VM.
        * Log into Vagrant enviroment and then move to this project folder and make sure all project files can be seen from this folder
        * Build ***Simple-REST-API*** into image
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker build -t restapi-demo .
            Sending build context to Docker daemon   982 kB
            Step 1/10 : FROM ubuntu
             ---> 7b9b13f7b9c0
            Step 2/10 : MAINTAINER Dapeng Jiao <harper1011@gmail.com>
             ---> Using cache
             ---> 5563f39da590
            Step 3/10 : WORKDIR /opt/script/restapi/
             ---> Using cache
             ---> 89a6eee1c6b1
            Step 4/10 : COPY SOURCES/*.py /opt/script/restapi/
             ---> Using cache
             ---> 5db0c2c6d834
            Step 5/10 : COPY SOURCES/requirements.txt /opt/script/restapi/
             ---> Using cache
             ---> 336d4c2e436e
            Step 6/10 : RUN apt-get update && apt-get -y upgrade && apt-get install -y python-dev python-pip curl
             ---> Using cache
             ---> 06a1b663302e
            Step 7/10 : RUN pip install --upgrade pip && pip install -r /opt/script/restapi/requirements.txt
             ---> Using cache
             ---> 45a02e367ac2
            Step 8/10 : EXPOSE 3000
             ---> Using cache
             ---> 75694895cb99
            Step 9/10 : HEALTHCHECK --interval=10s --timeout=2s CMD curl -f http://localhost:3000/api/v1/ || exit 1
             ---> Using cache
             ---> e8f5189550c5
            Step 10/10 : ENTRYPOINT python /opt/script/restapi/simple_rest_server.py '0.0.0.0' 3000
             ---> Using cache
             ---> 0c0af8cc3dd5
            Successfully built 0c0af8cc3dd5
            ```
        * Remove old containers if exist
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker rm $(sudo docker ps -a -q) -f
            ```
        * Run *RedisDB* service as a container
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker run -d --name redis -p 6379:6379 redis
            3285bf4697c44a07ff3a5a2cf3d7b268921d2aa76db2e90d4e3151dae366ef25
            ```
        * Run ***restapi*** servince in another container and link with existsing ***RedisDB*** container
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker run -p 3000:3000 --name restapi-demo -d --link redis:redis restapi-demo
            8ce91a765146d81473d5c7e91ebaca19846d8ba5517d9069d28783ce189b3434
            ```
        * After at least 10 seconds, check the status of containers, and make sure container named as ***restapi-demo*** health state is ***heathly***

            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker ps
            CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                   PORTS                    NAMES
            8ce91a765146        restapi-demo        "/bin/sh -c 'pytho..."   4 minutes ago       Up 4 minutes (healthy)   0.0.0.0:3000->3000/tcp   restapi-demo
            3285bf4697c4        redis               "docker-entrypoint..."   4 minutes ago       Up 4 minutes             0.0.0.0:6379->6379/tcp   redis
            ```
        * Check the ***restapi-demo*** container host IP and assign it to environment variable
        
            ```
            [vagrant@Simple-REST-API vagrant]$ REST_CONTAINER_IP=$(sudo docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' restapi-demo)
            [vagrant@Simple-REST-API vagrant]$ echo $REST_CONTAINER_IP
            172.17.0.3
            ```
        * Execute testcase from local VM towards to REST API running on container
        
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo python SOURCES/test_rest_server.py $REST_CONTAINER_IP
            .
            ----------------------------------------------------------------------
            Ran 1 test in 0.200s

            OK
            ```
         * Or if you want you can also execute testcase from another container
         
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo docker run -it --rm --name tester --link restapi-demo:restapi-demo -v "$PWD"/SOURCES/:/opt/script/restapi/ python:2 /bin/bash -c "pip install -r /opt/script/restapi/requ
            irements.txt; python /opt/script/restapi/test_rest_server.py $REST_CONTAINER_IP"
            ...
            Building wheels for collected packages: pprint, bottle
              Running setup.py bdist_wheel for pprint ... done
              Stored in directory: /root/.cache/pip/wheels/e7/b7/4c/20e1da81a0b945e20a68c56523843ef571c2eb435829b35c72
              Running setup.py bdist_wheel for bottle ... done
              Stored in directory: /root/.cache/pip/wheels/49/cf/37/132916b926fae01d6e27d94c0018e3ad07452ec3760e24a36a
            Successfully built pprint bottle
            Installing collected packages: pprint, bottle, urllib3, idna, certifi, chardet, requests, redis
            Successfully installed bottle-0.12.13 certifi-2017.4.17 chardet-3.0.4 idna-2.5 pprint-0.1 redis-2.10.5 requests-2.18.1 urllib3-1.21.1
            .
            ----------------------------------------------------------------------
            Ran 1 test in 0.129s

            OK
            ```
    * Docker all in one script:
        * Use provided Vagrantfile to init a CentOS VM.
        * Log into Vagrant enviroment and then move to this project folder and make sure all project files can be seen from this folder
        * Execute script in order to make container to be created and executed the same as *step by step* section include testing as well.

            ***This step take really loooog time(MAX 30mins) due to download images in backgournd***
            
            ```
            [vagrant@Simple-REST-API vagrant]$ sudo python scripts/docker-all-in-one.py
            rm: cannot remove ‘testing.log’: Text file busy

            Message from syslogd@localhost at Jun 21 13:30:56 ...
             kernel:unregister_netdevice: waiting for lo to become free. Usage count = 1
            .
            ----------------------------------------------------------------------
            Ran 1 test in 0.484s

            OK
            ```


In case there is any problem during your verification, please contact me via email.

BTW: There is a ".gitlab-ci.yml" which is used for auto CI&CD testing. In case you use GitLab you can use that as well. [GitLab CI](https://about.gitlab.com/features/gitlab-ci-cd/)
