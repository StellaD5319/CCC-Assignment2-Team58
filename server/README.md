## docker-compose

it used to compile the `flask docker` and `nginx docker`.

---
`flask docker`:

Directory: /app/, /app/config

port: 5000. Thread: 2, Process: 4. Expose: 5000.

---
`nginx docker`:

It should put the front information into /dist directory in docker (nginx).

Port: 8080 : 80. Expose: 8080.

Changes: 

Modify the nginx.conf from `normal loop` to `events`, it speeds up processing, and the response time of web.

---
`Scenario:` 

Nginx: put it into one instance in Docker;

Flask\_1: Put it with same instance with Nginx in Docker; upstream api { server flask\_app:5000 }

Flask\_2: Put it into another instance in Docker; upstream api { server FLASK\_APP2:5000 } FLASK\_APP2 --> public IP of this instance;

Flask\_3: Put it into another instance in Docker; upstream api { server FLASK\_APP3:5000 } FLASK\_APP3 --> public IP of this instance;

In here, it will need three instances.
