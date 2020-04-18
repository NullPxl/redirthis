# redirthis
Quick script to take a list of urls and payloads and see where each url redirects to when tested with each payload.
python 3.7+ (due to some asyncio/aiohttp features only being available in this version)

Created with the intention of being used with [ParamSpider](https://github.com/devanshbatham/ParamSpider)
```
>python3 redirthis.py --list urls.txt --payloads payloads.txt --keyword FUZZ

http://examplefakesite.com:80/55301089/download?t=//www.google.com/%2e%2e -> https://examplefakesite.com/ [301] -> https://www.google.com/ [302]
...

```
