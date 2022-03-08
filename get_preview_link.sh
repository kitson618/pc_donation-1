ip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
echo "NGINX URL"
echo "http://$ip:80"
echo "Flask App URL"
echo "http://$ip:5000"
echo "DB Admin URL"
echo http://$ip:8080
echo "Visualizer URL"
echo "http://$ip:8081"
