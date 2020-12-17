# build docker image
docker build -t prometheus-custom-fs-exporter .

# Run docker
docker run -p 8000:8000 prometheus-custom-fs-exporter 

# View in Browser
http://localhost:8000/metrics