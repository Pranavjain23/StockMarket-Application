Asterix and Double Trouble 

## Goals 

The Gauls have really taken to stock trading and trading has become their village pass time. To ensure 
high performance and tolerance to failures, they have decided to adopt modern design practices. 

1.  The stock bazaar application consists of three microservices: a front-end service, a catalog
    service, and an order service.

2.  The front-end service exposes the following REST APIs as they were defined in lab2:

    *   `GET /stocks/<stock_name>`
    *   `POST /orders`

    In addition, the front-end service will provide a new REST API that allows clients to query
    existing orders:

    *   `GET /orders/<order_number>`

        This API returns a JSON reply with a top-level `data` object with the four fields: `number`,
        `name`, `type`, and `quantity`. If the order number doesn't exist, a JSON reply with a
        top-level `error` object should be returned. The `error` object should contain two fields:
        `code` and `message`

3.  The interfaces used between the microservices. Each microservice
    handle requests concurrently.

4.  Added some variety to the stock offering by initializing your catalog with at least 10 different
    stocks. Each stock should have an initial volume of 100.

5.  The client first queries the front-end service with a random stock, then it will make a
    follow-up trade request with probability `p` (make `p` an adjustable variable). I
    decide whether the stock query request and the trade request use the same connection. The
    client will repeat the aforementioned steps for a number of iterations, and record the order
    number and order information if a trade request was successful. Before exiting, the client will
    retrieve the order information of each order that was made using the order query request, and
    check whether the server reply matches the locally stored order information.
