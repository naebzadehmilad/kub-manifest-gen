import time
from jinja2 import Template
import configparser
conf = configparser.ConfigParser()
import os
def config():
    global deploystate
    global deployname
    global hostaliases
    global ip
    global hostname
    global image
    global cpu
    global memory
    global port
    global volhpath
    global volhname
    global volcpath
    if os.path.exists('config.cfg'):
        print('##config.cfg is exist##.')
    else:
        conf.add_section("deployment")
        conf.set('deployment','state','True')
        conf.set('deployment','name','api-stg')
        conf.set('deployment','hostaliases','True')
        conf.set('deployment','ip','127.0.0.1')
        conf.set('deployment','hostname','example.local')
        conf.set('deployment','image','reg.example.local:5001')
        conf.set('deployment','cpu','1')
        conf.set('deployment','memory','1G')
        conf.set('deployment','port','80')
        conf.set('deployment','volume-host-path','/etc/localtime')
        conf.set('deployment','volume-host-name','time')
        conf.set('deployment','volume-container-path','/etc/localtime')
        with open('config.cfg', 'w') as configfile:
            conf.write(configfile)
            configfile.close()
    #read
    conf.read('config.cfg')
    deploystate = str(conf.get('deployment', 'state')).split(',')
    deployname = str(conf.get('deployment', 'name')).split(',')
    hostaliases= str(conf.get('deployment', 'hostaliases')).split(',')
    ip =str(conf.get('deployment', 'ip')).split(',')
    hostname=str(conf.get('deployment', 'hostname')).split(',')
    image=str(conf.get('deployment', 'image')).split(',')
    cpu=str(conf.get('deployment', 'cpu')).split(',')
    memory=str(conf.get('deployment', 'memory')).split(',')
    port=str(conf.get('deployment', 'port')).split(',')
    volhpath=str(conf.get('deployment', 'volume-host-path')).split(',')
    volhname=str(conf.get('deployment', 'volume-host-name')).split(',')
    volcpath=str(conf.get('deployment', 'volume-container-path')).split(',')

def deployment():
    f = open('{name}-deploy'.format(name=deployname[0]), "w")
    template = Template("""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{deployname}}
  labels:
    app: {{deployname}}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{deployname}}
  template:
    metadata:
      labels:
        app: {{deployname}}
    spec:
    {% if hostaliases == 'True' %}
      hostAliases:
      - ip: {{ip}}
        hostnames:
        - {{hostname}}
    {% endif %}
      containers:
      - name: {{deployname}}
        image: {{image}} 
        resources:
          requests:
            memory: {{memory}}
            cpu: {{cpu}}
          limits:
            memory: {{memory}}
            cpu: {{cpu}}
        ports:
        - containerPort: {{port}}
        volumeMounts:
        - mountPath: {{volcpath}}
          name: {{volhname}}
      volumes:
      - name: {{volhname}}
        hostPath:
          path: {{volhpath}}   
    """)
    f.write(template.render(deployname=deployname[0],hostaliases=hostaliases[0],ip=ip[0],hostname=hostname[0]
                            ,cpu=cpu[0],memory=memory[0],port=port[0],image=image[0],volcpath=volcpath[0],
                            volhname=volhname[0],volhpath=volhpath[0]))
    f.close()

config()
#if 'True' in deploystate[0] :
deployment()
