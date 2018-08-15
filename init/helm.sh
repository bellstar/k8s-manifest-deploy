set -e

[ ! -z $AZURE_SUBSCRIPTION_ID ] && \
[ ! -z $AZURE_TENANT_ID ] && \
[ ! -z $AZURE_CLIENT_ID ] && \
[ ! -z $AZURE_CLIENT_SECRET ] || ( echo "Required env was missing"; exit 1 )

echo "Try to Install 'Service Catalog'"

helm init --force-upgrade
sleep 1
helm repo add svc-cat https://svc-catalog-charts.storage.googleapis.com
helm install svc-cat/catalog --name catalog --namespace catalog --set rbacEnable=false

echo "Try to Install 'Open Service Broker for Azure'"
sleep 1
helm repo add azure https://kubernetescharts.blob.core.windows.net/azure
helm install azure/open-service-broker-azure --name osba --namespace osba \
    --set azure.subscriptionId=$AZURE_SUBSCRIPTION_ID \
    --set azure.tenantId=$AZURE_TENANT_ID \
    --set azure.clientId=$AZURE_CLIENT_ID \
    --set azure.clientSecret=$AZURE_CLIENT_SECRET

