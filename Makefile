.PHONY: install build deploy invoke start_dns lookup

PORT=53

install:
	brew install dnsmasq

build:
	samlocal build --use-container

deploy: build
	samlocal deploy --stack-name hello-world --resolve-s3

invoke:
	awslocal lambda invoke --function-name "hello-world-function" --payload '' --log-type Tail response.json | jq .LogResult -r | base64 -d && cat response.json | jq -r .result

start_dns:
	sudo dnsmasq --no-daemon --addn-hosts=localstack_hosts --port $(PORT) --listen-address=0.0.0.0

lookup:
	nslookup amazonaws.com 127.0.0.1 -port=$(PORT)
