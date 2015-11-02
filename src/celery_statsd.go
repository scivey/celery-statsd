package main

import (
    "github.com/quipo/statsd"
    "gopkg.in/redis.v3"
    "flag"
    "fmt"
    "runtime"
    "strings"
    "time"
)

var redisHostFlag = flag.String("redis-host", "localhost", "broker host")
var redisPortFlag = flag.Int64("redis-port", 6379, "broker port")
var statsdHostFlag = flag.String("statsd-host", "localhost", "statsd host")
var statsdPortFlag = flag.Int64("statsd-port", 8125, "statsd port")
var queueNamesFlag = flag.String("queues", "celery", "comma-separated list of queue names")
var statsPrefixFlag = flag.String("stats-prefix", "celery_queue_length", "prefix for metrics sent to statsd")
var intervalFlag = flag.Int64("interval", 5000, "polling interval (ms)")

func main() {
    flag.Parse()
    queueNames := strings.Split(*queueNamesFlag, ",")
    fmt.Println(queueNames)
    runLoop(*redisHostFlag, *redisPortFlag, *statsdHostFlag, *statsdPortFlag, *statsPrefixFlag, *intervalFlag, queueNames)
    runtime.Gosched()
}

func runLoop(redisHost string, redisPort int64, statsdHost string, statsdPort int64, statsPrefix string, interval int64, queues []string) {
    client := redis.NewClient(&redis.Options{
        Addr: fmt.Sprintf("%s:%d", redisHost, redisPort),
        DB: 10,
    })
    _, connErr := client.Ping().Result()
    fmt.Println("connection errors? ", connErr)

    statsdClient := statsd.NewStatsdClient(
        fmt.Sprintf("%s:%d", statsdHost, statsdPort),
        fmt.Sprintf("%s.", statsPrefix),
    )
    statsdClient.CreateSocket()
    stats := statsd.NewStatsdBuffer(time.Second * 2, statsdClient)
    defer stats.Close()
    timeoutInterval := time.Duration(interval) * time.Millisecond
    for true {
        for _, name := range queues {
            go func(oneName string) {
                listLength, err := client.LLen(oneName).Result()
                stats.Gauge(oneName, listLength)
                fmt.Println(oneName, listLength, err)
            }(name)
        }
        time.Sleep(timeoutInterval)
    }
}
