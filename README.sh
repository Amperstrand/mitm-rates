# mitm-rates

FQDNs=("customrates.local" "bylls.com" "api.coingecko.com")

echo "This is ment as a proof of concept. Don't run it in production of an idea explained here: https://github.com/btcpayserver/btcpayserver/discussions/2489#discussioncomment-7429013"

openssl genpkey -algorithm RSA -out certificates/MITM.key

#generate a selfsigned SSL cert
for fqdn in "${FQDNs[@]}"; do
    openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -key certificates/MITM.key -out certificates/${fqdn}.MITM.crt -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourDepartment/CN=${fqdn}"
done

#deploy the selfsigned SSL cert to btcpayserver
docker cp certificates/api.coingecko.com.MITM.crt generated-btcpayserver-1:/usr/local/share/ca-certificates/
docker cp certificates/bylls.com.MITM.crt         generated-btcpayserver-1:/usr/local/share/ca-certificates/
docker cp certificates/customrates.local.MITM.crt       generated-btcpayserver-1:/usr/local/share/ca-certificates/
docker exec -it generated-btcpayserver-1 update-ca-certificates

docker build -t mitm-rates .

#configure docker network so that generated-btcpayserver-1 can access mitm-rates-network
docker network create --driver bridge --subnet 192.168.99.0/24 mitm-rates-network
docker network connect mitm-rates-network generated-btcpayserver-1
docker run --network mitm-rates-network --ip 192.168.99.3 -d mitm-rates

# add the IP of ${FQDN} to generated-btcpayserver-1 so that it visits our server instead if it is not already there
#! docker exec generated-btcpayserver-1 grep -q ${FQDN} /etc/hosts && docker exec generated-btcpayserver-1 sh -c "echo '192.168.99.3 ${FQDN}' >> /etc/hosts"
! docker exec generated-btcpayserver-1 grep -q bylls.com /etc/hosts && docker exec generated-btcpayserver-1 sh -c "echo '192.168.99.3 bylls.com' >> /etc/hosts"
! docker exec generated-btcpayserver-1 grep -q customrates.local /etc/hosts && docker exec generated-btcpayserver-1 sh -c "echo '192.168.99.3 customrates.local' >> /etc/hosts"

#To clean up after testing this proof of concept, remember to remove the SSL cert and change remove ${FQDN} from /etc/hosts
