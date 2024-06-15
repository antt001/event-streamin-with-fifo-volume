# Non Blocking Producer/Consumer stream processer
## Summary
This is an implementation od a Non Blocking Producer/Consumer stream processing service that exposes an HTTP API. This is a quick solution using fifo buffer on the Docker shared volume(ipc) for inter process comunication. Docker compose have 2 containesrs: producer and consumenr. 

Consumer container is depended on the producer and will start afterwars. It will agreate the events in the dict datastructure in a separate daemon thread in order to separaate reads and writes and not block the main thread. The aggeration data will be available on the http rest api endpoints, as it is populated.

Producer container will first create the Fifo stram file using mkfifo linux command and then will start the producer.py script(_in unbuffered output mode_) redirecting the output to the fifo stream.

## Usage
Navigate the the project root folder, start docker compose in the daemon mode
```bash
docker compose up -d
```
The http rest api server will be available on port 5000
access event count:
```bash
curl --location 'http://localhost:5000/events/countByEventType'
```
access word count:
```bash
curl --location 'http://localhost:5000/events/countWords'
```

## Improvement suggestions
In order to achive horizontal scalability, we can separate the consumer and the API server in difernt containers and utilize the queues like SQS or streaming infra like kafka to stream the events.

- separate the consumer and the API server into different containers
- use queues like SQS or kafka to stream the events
- aggrete the events in redis with atomic increments(or use ksqlDB in case of kafka)

## Troubleshooting
If you ran into issues, please try to recreate the docker containers and the volumes:
```bash
docker compose down
docker volume ls
## look for your ipc volume, usualy named [my_folder]_ipc, and delete it
docker volume rm lynxmd_ipc
```
then run `docker compose up -d` again. 

If the above instructions do not help, please check the docker compose and container logs to investigate the issue.