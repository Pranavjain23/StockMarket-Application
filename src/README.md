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

## A brief design document

### REST APIs
1.  Front-end Service

    The front-end service exposes 3 different REST APIs to the clients:

    *   `GET /stocks/<stock_name>`
    *   `POST /orders`
    *   `GET /orders/<order_number>`

    `GET /stocks/<stock_name>` allows clients to query the current price of stocks; `POST /orders` allows clients to place an order; `GET /orders/<order_number>` allows clients to query existing orders saved in the order server database.

2. Order Service

    The order service exposes the following APIs to allow the front-end to query existing orders and allow the replicas to synchronize with each other:

    *   `GET /orders/<order_number>`
    *   `POST /orders`
    *   `GET /synchronize`
    *   `POST /propagate`
    
    `GET /orders/<order_number>` returns previous order information according to the given order number; `POST /orders` forwards the order request the the catalog service; `GET /synchronize` allows a replica coming back online from a crash to ask the other replicas for the latest order number; `POST /propagate` allows the leader node to propagate the information of a sucessful trade to the follower nodes. 

3. Catalog Service

    The catalog service maintains the following APIs:

    *   `GET /stocks/<stock_name>`
    *   `POST /orders`
    *   `POST /invalidation/<stock_name>`

    Calliing `POST /orders` and `GET /stocks/<stock_name>` will update and return the data in the catalog database, as they were defined in the lab2. `POST /invalidation/<stock_name>` will be sent to the frontend server whenever there is a successful order, so the frontend can remove the invalid stock information from its cache. 


### Caching
The front-end server maintains a in-memory LRU cache the records the stock information of the last n `GET /stocks/<stock_name>` requests. Upon receiving a stock query request, it first checks the cache to see whether it can be served from the cache. If not, the request will then be forwarded to the catalog service, and the result returned by the catalog service will be stored in the cache. Cache consistency is maintained by `POST /invalidation/<stock_name>`, which causes the front-end service to remove the corresponding stock from the cache.

### Replication & Consistency
Each order replica will open a socket, and the front-end service will contact each replica via the socket to perform leader selection. The front-end maintains a `leader_selection()` function, which will send a "Ping" message to each reaplica, staring from the node with the highest ID, and then wait for the responses. Upon receiving the first "OK" reply from the node, the front-end will asign it as the leader and nofity the result towards other replicas. 

#### Propagation
When a trade request or an order query request arrives, the front-end service only forwards the request to the leader. In case of a successful trade, the leader node will propagate the information to the follower nodes by sending a `POST /propagate` request to the follower nodes.

### Fault Tolerance
When the front-end service finds that the leader node is unresponsive, it will redo the leader selection process. In our design, this is achieved by two mechanisms: a passive health check and an actively regular health check.

#### Passive health check
Whenever the front-end forwards a request to the leader, it uses a try-except block to capture the `requests.exceptions.RequestException`. In case of a connection failure, the front-end will call `leader_selection()` to start a leader selection, finding an alive replica, broadcasting the new leader, and then redirect the reqeust to it. 

#### Active health check
The frontend will regularly send "PING" to the current leader to see if the leader is alive. The time interval between each active health check can be changed in the configuration file. If the leader has no response, the frontend will restart leader selection to find an available order server of the hightest ID.

#### Resuming mechanism
When a replica comes back online from a crash, it will frist look at its database file to get the latest order number that it has. After that, it will send a `GET /synchronize` request to its peers, which return the latest order number saved in their database. Thus, the resuming replica knows exactly what's the orders it has missed since the previous crash. Afterwards, it will send sequential `GET /orders/<order_number>` requests to the node that maintains the latest order information to acquire the missing orders.
