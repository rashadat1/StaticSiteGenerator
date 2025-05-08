# How I Built Redis from Scratch (and the Shit Ton I Learned Doing It)

[< Back Home](/)

---

_The planned structure is to write this high-level overview and link to more detailed articles within the body of this text_

Though this is without a doubt the project that set me down the path of building everything from scratch as a way of learning - even at the outset of this project - I didn't set out to build a full-fledged Redis clone. I actually started this project as a way to learn Java as I've always been someone who learns best by doing. Nevertheless - this is a high level overview of what I built, what broke (what nearly caused me to give up), and what I learned along the way. As the first project I undertook in my journey as a Software Engineer - it is only fitting that I kick off this blog with Redis.

This is a deep dive into what I built, what broke, and what I learned along the way.

## Building the Basics

### Binding to a Port

The journey began with the fundamentals of TCP, socket programming, and building a RESP (Redis Serialization Protocol) parser. The first step is to open up a server socket and bind it to port 6379. This socket will "listen" on the port - waiting for a new client connection. When the server socket receives a request to connect from a client - a new client socket is created that allows for two way communication between the server and client. 

In your main loop this looks like:

```
try (ServerSocket serverSocket = new ServerSocket(port)) {
    serverSocket.setReuseAddress(true)
    while (true) {
        Socket clientSocket = serverSocket.accept();
    }
}
```

### RESP Basics

Redis clients communicate with Redis servers by sending commands - which are RESP encoded strings (don't worry we'll get to RESP in a sec). PING is the simplest of the Redis commands and while we start with this command to prove bytes are being received and sent correctly through the channel between the client and server we opened above, we later use them to check if a Redis server is healthy or to initiate a master-slave connection - but we will get to that.

When a Redis server receives a PING command - the expected response is ```+PONG\r\n``` which is the string PONG encoded using RESP. RESP allows us to serialize different data types - integers, strings, arrays, and even its own special type for errors. Clients send requests to the Redis server as an array of strings - strings representing the command to be executed and the data against which to execute the commands. The server's reply type is command-specific. Requests and responses are pipelined - which allows a client to send multiple commands at once and wait for replies later - there is also a concept of transactions in Redis - where we queue transactions to be executed in sequence at a later date. 

Now, we should probably start talking about RESP. RESP is the formatting protocol that clients implement in order to communicate with a Redis server. It has the advantage of being simple to implement, human readable, and fast to parse.

The first byte in a RESP-serialized payload is always the data type of the encoded data. The CRLF (\r\n) is the protocol's terminator and also used to separator the multiple "parts" of an RESP payload. What this allows us to do is - with the first byte - determine the data type that a Redis server or Redis client has sent and from there decide how to process or store the value in memory.

The most important data types for our purposes are Simple Strings, Simple Errors, Integers, Bulk Strings, and Arrays.

#### Simple Strings

Simple Strings are encoded with their first byte the character (+). They are then immediately followed by a single string value that cannot contain CR (\r) or LF (\n). They are then terminated with CRLF. The Simple String:
```+OK\r\n``` 
is often used by Redis server to respond to the client when a command that does not require data to be returned to the client is successfully executed such as setting a key-value pair with the SET command.

#### Simple Errors

Similarly, Simple Errors are encoded using their custom identifying byte value (in this case -) and then an error message that terminates with CRLF:

```-ERR: Cannot increment array value\r\n```

As you could probably guess - Simple Errors are returned to the client when something went wrong while processing a command.

#### Integers

Integers have : as their first byte and are followed by an optional + or - as the sign and then a 64-bit integer and (surprise surprise) are terminated with \r\n:

```:324\r\n```

#### Bulk Strings

Bulk Strings are similar to Simple Strings - they encode string data - but Bulk Strings are allowed to contain any characters including newlines, control characters, and can be configured to have any length. The prefix $ is used followed by the length of the string data separated by CRLF:

```$13\r\nTarik Rashada\r\n```

Bulk Strings also have a special null value which is used fairly often when responding to requests that don't raise an error but often return empty data

```$-1\r\n```

#### Arrays

Arrays are probably the most important type as they are the encoding format that clients use to send commands to the Redis server and how the Redis server encodes and sends some replies that themselves return arrays (e.g. XRANGE and LRANGE which read and return elements of a stream and list respectively). The first byte is * and the rest of the string is encoded this way

```*<number_of_elements>\r\n<RESP for element-1>...<RESP for element-n>\r\n```

We can nest arrays to return index-keyed associative arrays with this format, or sends arrays of multiple Bulk Strings or integers and even mix data types. So for instance, if for some reason we wanted to encode an array whose elements 

```"I think therefore I am".split(" ")```

encoded as Bulk Strings we would have:

```*5\r\n$1\r\nI\r\n$5\r\nthink\r\n$9\r\ntherefore\r\n$1\r\nI\r\n$2am\r\n```


More information about RESP can be found here:

[RESP](https://redis.io/docs/latest/develop/reference/protocol-spec/#resp-simple-strings)
