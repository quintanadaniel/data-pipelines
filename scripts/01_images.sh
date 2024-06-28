docker build -t outlier-detection:v1 -f Dockerfile.outlier_detection_v1 .
docker build -t outlier-detection:v2 -f Dockerfile.outlier_detection_v2 .
k3d image load outlier-detection:v1 -c test-cluster
k3d image load outlier-detection:v2 -c test-cluster