from fastapi import Request
import time


async def client_authentication(request: Request, call_next):
    request_body = await request.json()
    print(request_body)
    # logger.info(
    #     f"{request.method} request to {request.url} metadata\n"
    #     f"\tHeaders: {request.headers}\n"
    #     f"\tBody: {request_body}\n"
    #     f"\tPath Params: {request.path_params}\n"
    #     f"\tQuery Params: {request.query_params}\n"
    #     f"\tCookies: {request.cookies}\n"
    # )
    start_time = time.time()
    response =  await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
