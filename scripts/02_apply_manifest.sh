kubectl apply -f Manifests/01_pvc_extract.yml
kubectl apply -f Manifests/02_pvc_transform.yml
kubectl apply -f Manifests/03_pvc_load.yml
kubectl apply -f Manifests/04_pod_extract.yml
sleep 5
kubectl apply -f Manifests/05_pod_transform.yml
sleep 5
kubectl apply -f Manifests/06_pod_load.yml
sleep 5
kubectl apply -f Manifests/07_pod_list_files.yml