# -*- coding: utf-8 -*-
import yaml, json
import time
import os, sys
import subprocess, json
# kubectl config view -o json | jq '.["current-context"]'

e = os.environ

argv = sys.argv
if len(argv) != 2:
    print "{} your_namespace".format(argv[0])
    sys.exit()

NAMESPACE = argv[1]
DOMAIN = "{namespace}.svc.cluster.local".format(namespace=NAMESPACE)
RP_BACKEND = "mywebsample"
NOTIFY_URI = "http://mynotifypod/api/slack"
API_HOST   = "myappsample"
MONGODB_URI = "mongodb://mongodb.examplev.info:50001"
# MONGODB_HOST = "mongodb.examplev.info"
# MONGODB_PORT = "50001"
SLACK_URI    = e.get('SLACK_URI')

config_view = json.loads(subprocess.check_output("kubectl config view -o json".split(" ")))
DEFAULT_NS = config_view['current-context']

subprocess.call("kubectl create namespace {}".format(NAMESPACE).split(" "))
subprocess.call("kubectl config set-context {} --namespace {}".format(DEFAULT_NS, NAMESPACE).split(" "))

cmds="""
---
- name: コメント用 APIサーバをデプロイ
  cmd:
    - kubectl run myappsample --image shkawan/appsample:v5.00 --env=MONGODB_URI={MONGODB_URI}
    - kubectl expose deployment myappsample --port=80 --type=ClusterIP

- name: アプリ表示用 Webアプリケーションをデプロイ
  cmd:
    - kubectl run mywebsample --image shkawan/websample:v0.75 --env=API_HOST={API_HOST} --env=NOTIFY_URI={NOTIFY_URI}
    - kubectl expose deployment mywebsample --port=80 --type=ClusterIP

- name: リバースプロキシ simple-reverseproxyをデプロイ
  cmd: 
    - kubectl run myreverseproxy --image shkawan/simple-reverseproxy:v0.03 --env=RP_BACKEND={RP_BACKEND}.{DOMAIN}
    - kubectl expose deployment myreverseproxy --port=80 --type=LoadBalancer

- name: 通知用Podをデプロイ
  cmd:
    - kubectl create deployment mynotifypod --image shkawan/notifyservice:v0.84 --image shkawan/docker-postfix:v0.01
    - kubectl expose deployment mynotifypod --port=80 --type=ClusterIP
    - kubectl set env deployment mynotifypod -c notifyservice SLACK_URI={SLACK_URI}

""".format(SLACK_URI=SLACK_URI, RP_BACKEND=RP_BACKEND, MONGODB_URI=MONGODB_URI, DOMAIN=DOMAIN, API_HOST=API_HOST, NOTIFY_URI=NOTIFY_URI)

for v in yaml.load(cmds):
    print v.get("name").encode("utf-8")
    for r in v.get("cmd"):
        print r
        yn = raw_input()
        if yn == "n":
            continue
        else:
            subprocess.call(r.split(" "))
        print
    print "------------------------------------"
    time.sleep(2)
    print "Next ?"
    raw_input()


subprocess.call("kubectl config set-context {} --namespace {}".format(DEFAULT_NS, "default").split(" "))
