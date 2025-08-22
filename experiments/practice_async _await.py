import asyncio 

async def say_hello():
    print("hello world")
    await asyncio.sleep(1)  
    print("hello again") 
asyncio.run(say_hello())
    