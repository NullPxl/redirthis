import asyncio
import aiohttp
import os
import sys
import argparse

from aiohttp import ClientSession


os.system('') # let colours be used
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


async def gen_tasks(session, urls, payloads, keyword):

    with open(urls) as u:
        urls = u.read().splitlines()
    with open(payloads) as p:
        payloads = p.read().splitlines()

    tasks = []
    for url in urls:
        for payload in payloads:
            task = asyncio.ensure_future(getResponse(session, url, payload, keyword))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def getResponse(session, url, payload, keyword):

    r_url = url.replace(keyword, payload)
    async with session.get(r_url, allow_redirects=True, timeout=10) as response:
        history = response.history
        locations = f"{r_url}"
        if response.history:
            for r in history:
                location = str(r).split("Location': \'")[1].split("\'")[0]
                if history[-1] == r:
                    locations += f" -> {bcolors.OKGREEN}{location}{bcolors.ENDC} [{r.status}]"
                else:
                    locations += f" -> {location} [{r.status}]" 
            print(locations)
        else:
            pass

async def redirme(url_list, payload_list, keyword):
    async with aiohttp.ClientSession() as session:
        await gen_tasks(session, url_list, payload_list, keyword)

def main():

    parser = argparse.ArgumentParser(description="test a list of payloads on a list of sites to track redirect history")
    parser.add_argument('-l', '--list', help='file of domains to test', required=True)
    parser.add_argument('-p', '--payloads', help='file of payloads', required=True)
    parser.add_argument('-k', '--keyword', help='keyword in urls to replace with payload (default is FUZZ)', default="FUZZ")
    args = parser.parse_args()

    if os.name=="nt" and sys.version_info[:2] == (3, 8):
        # https://github.com/aio-libs/aiohttp/issues/4324
        # looks like there's some issues with python 3.8+ on windows and asyncio, until a fix comes suppressing errors works.
        class DevNull:
            def write(self, msg):
                pass
        sys.stderr = DevNull()

    # TODO: make a more extensive payload list (generate from domain: https://github.com/cujanovic/Open-Redirect-Payloads)
    asyncio.run(redirme(args.list, args.payloads, args.keyword))

if __name__ == "__main__":
    main()
