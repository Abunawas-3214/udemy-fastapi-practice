from fastapi.requests import Request

def log(tags="MyApp", message="", request: Request = None):
    with open("log.txt", "a+") as log:
        log.write(f"{tags}: {message}\n")
        log.write(f"\t{request.url}\n")