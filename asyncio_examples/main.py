import asyncio

async def worker(callback):
    while True:
        # Simulate some work
        await asyncio.sleep(1)

        # Produce a value and notify the main loop
        value = "Some data from the worker"
        await callback(value)

async def process_data(value):
    # Process the received data in the main loop
    print(f"Received data from worker: {value}")

async def main():
    # Start the worker in the background, passing the callback function
    asyncio.create_task(worker(process_data))

    # Main loop continues with other tasks or activities
    while True:
        # Simulate other activities in the main loop
        print("Main loop is doing something else.")
        await asyncio.sleep(2)

# Run the main loop
asyncio.run(main())