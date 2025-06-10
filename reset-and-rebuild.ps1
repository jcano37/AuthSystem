# Stop and remove all containers
docker-compose down --volumes --remove-orphans

# Remove all images related to this project (edit the grep if your image name is different)
$images = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "authsystem|auth-service"
foreach ($img in $images) {
    docker rmi -f $img.ToString().Trim()
}

# Remove all dangling images (optional cleanup)
docker image prune -f

# Remove all volumes related to this project
docker volume prune -f

# Rebuild and start containers in the background
docker-compose up --build -d

# Wait for containers to be healthy (adjust the sleep if needed)
Start-Sleep -Seconds 10

# Run a fresh Alembic migration inside the app container
docker-compose exec app alembic upgrade head
