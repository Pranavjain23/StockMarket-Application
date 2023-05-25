## How to run

#### Run the services locally
To run the three services and two additional order replicas, we need to open 6 termninals.

In terminal 1:
```shell
cd src/catalog
python3 catalog.py --config ../config.yaml 
```

In terminal 2:
```shell
cd src/order
python3 order.py --config ../config.yaml --id 3
```

In terminal 3:
```shell
cd src/order
python3 order.py --config ../config.yaml --id 2
```

In terminal 4:
```shell
cd src/order
python3 order.py --config ../config.yaml --id 1
```

In terminal 5:
```shell
cd src/frontend
python3 frontend.py --config ../config.yaml
```

In terminal 6, run the client:
```shell
cd src/client
python3 client.py --n_request 1000 --host 0.0.0.0 --port 8080 --prob 0.5
```
Or, run multiple clients concurrently:
```shell
cd src/client
./run_multi_client.sh 0.0.0.0 8080 1000 0.2
```

### Run services using Docker

1. Assign the variables, such as host, ports, cache size, database file location, etc., in `.env`.
```shell
CATALOG_HOST=my_catalog
CATALOG_PORT=8087
ORDER_HOST3=my_order3
ORDER_PORT3=16008
ORDER_LEADER_BROADCAST_PORT3=16018
ORDER_HEALTH_CHECK_PORT3=16028
ORDER_HOST2=my_order2
ORDER_PORT2=16007
ORDER_LEADER_BROADCAST_PORT2=16017
ORDER_HEALTH_CHECK_PORT2=16027
ORDER_HOST1=my_order1
ORDER_PORT1=16006
ORDER_LEADER_BROADCAST_PORT1=16016
ORDER_HEALTH_CHECK_PORT1=16026
FRONTEND_HOST=my_frontend
FRONTEND_PORT=8080
OUTPUT_DIR=/data
HEALTH_CHECK_INTERVAL=0.5
CACHE_SIZE=5
CACHE_LOG_PATH=/data/log.json
```
2. Use Docker Compose to build the three services and their replicas (on root)
```shell
docker compose up
```
3. Run the client
```shell
python3 src/client/client.py --n_request 500 --host 0.0.0.0 --port 8080 --prob 0.2
```

### To test fault tolerance
During the sequential requests, you can press ctrl+c to shutdown any one of the order replicas. As long as there is at least one server replica alive, the whole application will still work. 

Assume that you just shut down the order server with ID=3, you can restart that server by adding the `--resume` argument:
```shell
python3 order.py --config ../config.yaml --id 3 --resume
```
You can shut down and bring back the order server several times as the client is still sending its sequential requests to the frontend.

After the client exists, check the three order database files in `src/order/data`. The order information in each file should be consistent.