
helm init --upgrade
sleep 10

echo "Setup 'Service Catalog'"
helm repo add svc-cat https://svc-catalog-charts.storage.googleapis.com
helm install svc-cat/catalog --name catalog --namespace catalog --set rbacEnable=false

