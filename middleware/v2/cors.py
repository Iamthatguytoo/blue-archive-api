from fastapi.middleware.cors import CORSMiddleware

def setup_cors(server):
    server.add_middleware(
        CORSMiddleware,
        allow_credentials=False,
        allow_origins = ["*"],
        allow_methods = ["GET", "POST", "OPTIONS"],
        allow_headers = ["x-api-key", "Content-Type", "Authorization"],
    )