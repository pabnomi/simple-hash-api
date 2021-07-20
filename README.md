# simple-hash-api
Very simple python application using only standard library, 
serves an HTTP endpoint that stores and returns the SHA256 hash of a string sent as json payload.  
_Playing with Github Actions syntax and options._

#### Endpoints
**/messages**  
Accepts a JSON message as POST. Following this format:

```
{
  "message": "this is a sample message!"
}
```

```
curl -X POST -H 'Content-Type: text/json' -d '{ "message": "Test message" }' localhost:8080/messages
# returns
{
  "digest": "c0719e9a8d5d838d861dc6f675c899d2b309a3a65bb9fe6b11e5afcbf9a2c0b1"
}
```

**/messages/\<hash\>**
Accepts the SHA256 of a message as a GET parameter and returns the content of the original message as a string.

```
curl localhost:8080/messages/c0719e9a8d5d838d861dc6f675c899d2b309a3a65bb9fe6b11e5afcbf9a2c0b1
{
  "message": "Test message"
}
```

**/metrics**  
Returns information about the service in JSON format  
WIP



### Running it locally

```bash
# clone the repository
docker build -t simple-hash-api:v0.0.1 .
docker run -p 8080:8080 --rm --name simple-hash-api simple-hash-api:v0.0.1
```

