import json
import os

import yaml
import aiohttp
from fastapi import FastAPI

PANGOLIN_ADDRESS = os.getenv("PANGOLIN_ADDRESS", 'http://pangolin:3001/api/v1/traefik-config')
OVERRIDE_FILE = os.getenv("OVERRIDE_FILE", '/app/override_headers.yaml')

app = FastAPI()

async def pangolin_traefik_config():
    async with aiohttp.ClientSession() as session:
        async with session.get(PANGOLIN_ADDRESS) as response:
            return json.loads(await response.text())

@app.get('/api/v1/traefik-config')
async def traefik_config():
    pangolin_config = await pangolin_traefik_config()

    if override_config is None:
        return pangolin_config
    
    for k, v in override_config.items():
        pangolin_config["http"]["middlewares"][f"headers-{k}"] =  {"headers": {"customRequestHeaders": v}}

    routers = pangolin_config["http"]["routers"]
    if len(routers) < 1:
        return pangolin_config
    for k, v in routers.items():
        if k.endswith('redirect'):
            continue
        domain = v["rule"][6:-2]
        if domain not in override_config:
            continue
        v["middlewares"].append(f"headers-{domain}")

    return pangolin_config

if __name__ == '__main__':
    import uvicorn
    global override_config

    with open(OVERRIDE_FILE, 'r') as f:
        override_config = yaml.safe_load(f)

    uvicorn.run(app, host='0.0.0.0', port=3001)