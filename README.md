# Pangolin Header Patcher

## Installation

Either build the container yourself or use the one that is build by the workflow from this repo.
Create a config file that matches the syntax in the following example. Note that the key needs to be the domain you are using for the service and the content is a map of headers that will be passed through.
So anything written under the key is used ad verbum.
```yaml
domain.one:
  Authorization: "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
domain.two:
  Authorization: "Basic YW5vdGhlcnVzZXI6YW5vdGhlcnBhc3N3b3Jk="
  Whatever: "You-Feel-Like"
```

Add the container to your pangolin compose stack. E.g. like the following code block. The path to the file within the container can be overriden bei the environment variable `OVERRIDE_FILE`. The API address of the traefik config can also be overriden by using the environment variable `PANGOLIN_ADDRESS` if necessary.

```yaml
# [...]
  patcher:
    image: ghcr.io/lhw/pangolin-patcher:main
    container_name: patcher
    restart: unless-stopped
    depends_on:
      - pangolin
    volumes:
      - ./patcher.yml:/app/override_headers.yaml
# [...]
```

Then update the static treafik configuration file so that the http provider endpoint now points to the patching service. Like this:
```yaml
# [...]

providers:
  http:
    endpoint: "http://patcher:3001/api/v1/traefik-config"

# [...]
```
Leave all other values untouched.

Start the containers and restart traefik and it should work immediately. Note that changes to the patcher yaml will require a container restart as the script is not watching file changes yet.
