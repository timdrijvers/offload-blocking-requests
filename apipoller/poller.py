import asyncio
from datetime import datetime, timedelta

import aiohttp
import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response


app = Starlette(debug=True)
POLL_TIMEOUT = timedelta(seconds=120)
conn_timeout = aiohttp.ClientTimeout(total=10)
POLL_INTERVAL = 1.0


async def fetch(session, poll_id):
    url = 'http://nginx/poll/{}/0'.format(poll_id)
    async with session.get(url) as response:
        return response.status, await response.text()


async def poll(poll_id):
    max_end_time = datetime.now() + POLL_TIMEOUT
    while datetime.now() < max_end_time:
        async with aiohttp.ClientSession(timeout=conn_timeout) as session:
            status, text = await fetch(session, poll_id)
            if 200 <= status < 300:
                return status, text
            if status != 400:
                break

        await asyncio.sleep(POLL_INTERVAL)
    return 423, 'failed'


@app.route('/poll/{id}')
async def single_poller(request):
    status, text = await poll(request.path_params['id'])
    return Response(text, status)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5500)
