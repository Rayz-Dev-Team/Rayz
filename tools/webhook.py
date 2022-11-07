import aiohttp
import json
import asyncio

EXAMPLEjsondata={
  "content": "Message content",
  "embeds": [
    {
      "title": "Body Title",
      "description": "Body description",
      "url": "https://optionalurl.com",
      "color": 5814783, # see this converter for hex color code: https://www.binaryhexconverter.com/hex-to-decimal-converter
      "fields": [
        {
          "name": "Field Example",
          "value": "Field Example"
        }
      ],
      "author": {
        "name": "Author",
        "url": "https://optionalurl.com",
        "icon_url": "https://optionalurl.com"
      },
      "footer": {
        "text": "footer",
        "icon_url": "https://optionalurl.com"
      },
      "timestamp": "2022-11-30T05:00:00.000Z",
      "image": {
        "url": "https://optionalurl.com"
      },
      "thumbnail": {
        "url": "https://optionalurl.com"
      }
    }
  ],
  "username": "Username (optional)",
  "avatar_url": "https://optionalurl.com",
  "attachments": []
}


async def async_send(webhook:str, jsondata:str|dict):
    '''
    Send data to a webhook, guilded or discord.
    '''
    try:
        if type(jsondata) == str:
            jsondata = json.loads(jsondata)
        elif type(jsondata) == dict:
            pass
    except:
        class InvalidJsonData(Exception):
            pass
        raise InvalidJsonData(f'Invalid json data passed into function async_send')
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url=webhook, data=jsondata) as p:
                response = await p.text()
                await p.close()
                return response
    except:
        raise aiohttp.InvalidURL('Invalid URL/Webhook passed.')

def sync_send(webhook:str, jsondata:str|dict):
    '''
    It is recommended to directly use async_send, as it skips any sketchy asyncio loop editing and running.
    '''
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_send(webhook=webhook,jsondata=jsondata))
    except:
        try:
            return asyncio.run(async_send(webhook=webhook,jsondata=jsondata))
        except Exception as e:
            raise e