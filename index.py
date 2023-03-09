from random import choices
import click
import inquirer
import os
from os import read, write, chdir, system 
from pathlib import Path
# import yaml

chartName=str(input("your chart name: "))
servicePort=int(input("your service port: "))
internalPort=int(input("your internalPort: "))
serviceType=str(input("your service type: "))
repo=str(input("your repository: "))
tag=str(input("your image tag: "))
pullSecret=str(input("your pullSecret: "))
helthCeckPath=str(input("your helthCeckPath: "))
livens=int(input("your livenessProbePeriodSeconds: "))
limitCpu=int(input("your limitCpu: "))
limitMemory=int(input("your limitMemory: "))
requestCpu=int(input("your requestCpu: "))
requestsMemory=int(input("your requestsMemory: "))

globalData = """
global:
    fullnameOverride: {chartName} 
    servicePort: {servicePort}
    internalPort: {internalPort}
    serviceType: {serviceType}
    livenessProbePeriodSeconds: {livens}
    repository: {repo}
    tag: {tag}
    pullSecret: {pullSecret}
    limit:
        cpu: {limitCpu}
        memory: {limitMemory}
    requests: 
        cpu: {requestCpu}
        memory: {requestsMemory}
"""

data="""

# ==================================== Deployment section ====================================

hi:
  fullnameOverride: "{{ .Values.global.fullnameOverride }}"
  
  containers:
    container:
    image:
      repository: "{{ .Values.global.repository }}"
      tag: "{{ .Values.global.tag }}"
      imagePullPolicy: Always
      imagePullSecrets: "{{ .Values.global.pullSecret }}"
      ports:
        - containerPort: "{{ .Values.global.servicePort }}"
    livenessProbe:
      httpGet:
      path: "{{ .Values.global.helthCeckPath }}"
      port: "{{ .Values.global.internalPort }}"
      periodSeconds: "{{ .Values.global.livenessProbePeriodSeconds }}"
    readinessProbe:
      httpGet:
      path: "{{ .Values.global.helthCeckPath }}"
      port: "{{ .Values.global.servicePort }}"

        # env:
        # volumeMounts:
        #     config-dir:
        #       mountPath: /prediction/resources

        #   volumes:
        #     config-dir:
        #       emptyDir: {}
        #     scripts-directory:
        #       configMap:
        #         name: "{{ .Values.global.fullnameOverride }}"-scripts

    resources:
      limits:
      cpu: "{{ .Values.global.limit.cpu }}"
      memory: "{{ .Values.global.limit.memory }}"
      requests:
      cpu: "{{ .Values.global.requests.cpu }}"
      memory: "{{ .Values.global.requests.memory }}"



        
  
service:
  type: {serviceType}
  port: "{{ .Values.global.servicePort }}"
  targetPort: "{{ .Values.global.internalPort }}"

  env:
    NAMESPACE               : {valueFrom: {fieldRef:        {fieldPath: metadata.namespace                                    }}}


# ==================================== Configmap section ====================================
mlPrediction-config:
  definitions:
    prediction-config:
      host: "{{ .Values.global.fullnameOverride }}.{{ .Release.Namespace }}"
      port: "{{ .Values.global.servicePort }}"
      uri: "http://{{ .Values.global.fullnameOverride }}.{{ .Release.Namespace }}:{{ .Values.global.servicePort }}"
      fullUri: "http://{{ .Values.global.fullnameOverride }}.{{ .Release.Namespace }}.svc.cluster.local:{{ .Values.global.servicePort }}"

"""

chartData="""
apiVersion: v2
name: {chartName}
description: A Helm chart for Kubernetes

appVersion: "0.1.0"
version: 0.1.0

dependencies:
- name: multi-app
  version: ">=0.1.0 <1.0.0"
  repository: "file://../templates/multi-app"
  alias: {chartName}
  condition: {chartName}.enabled
- name: configmap
  version: ">=0.1.0 <1.0.0"
  repository: "file://../templates/configmap"
  alias: {chartName}-config
  condition: {chartName}.enabled
"""




print(chartName)
os.system("helm create {}".format(chartName))
chdir(chartName)

with open('chart.yaml', 'w') as yfile:
    yfile.write(chartData.format(chartName=chartName))

os.system("rm -rf templates")
os.system("helm dependency build")
  
with open('values.yaml', 'w') as yfile:
    yfile.write(globalData.format(chartName=chartName,servicePort=servicePort,internalPort=internalPort,serviceType=serviceType,repo=repo,tag=tag,pullSecret=pullSecret,livens=livens,helthCeckPath=helthCeckPath,limitCpu=limitCpu,limitMemory=limitMemory,requestCpu=requestCpu,requestsMemory=requestsMemory))
    
with open('values.yaml', 'a') as yfile:
    yfile.write(data.format(serviceType=serviceType))






