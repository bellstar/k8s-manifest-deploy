#!/bin/bash

AKS_NAME=$AKS_NAME
RESOURCE_GROUP=$AKS_RESOURCE_GROUP
REGION=eastus
CONNECTOR_NAME=shkawan-vk

az aks install-connector -n $AKS_NAME --connector-name $CONNECTOR_NAME -g $RESOURCE_GROUP -l $REGION
