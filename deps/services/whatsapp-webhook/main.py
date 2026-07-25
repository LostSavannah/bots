from typing import Annotated
from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.responses import Response
import uvicorn, uuid, os

app = FastAPI()

parameters = {
    "TOKEN" : (TOKEN := os.environ.get("API_TOKEN", str(uuid.uuid4()))),
    "HOST" : (HOST := os.environ.get("API_HOST", "0.0.0.0")),
    "PORT" : (PORT := int(os.environ.get("API_PORT", "8080")))
}

print(parameters)

events = {}

class WhatsappApplication:
    def __init__(self, token):
        self.token = token
        self.events = {}

    def register_router(self, router:APIRouter) -> APIRouter:
        router.get("")(self.challenge)
        router.post("")(self.event)
        router.get("/events")(self.get_events)
        router.get("/events/:id")(self.get_event)
        router.delete("/events/:id")(self.delete_event)
        return router

    def challenge(
        self,
        hub_mode: Annotated[str | None, Query(alias="hub.mode")] = None,
        hub_challenge: Annotated[str | None, Query(alias="hub.challenge")] = None,
        hub_verify_token: Annotated[str | None, Query(alias="hub.verify_token")] = None
    ):
        if hub_verify_token != TOKEN or hub_mode != "challenge":
            return Response("UNAUTHORIZED", 401)
        return Response(hub_challenge, 200)

    async def event(
        self,
        req:Request
    ):
        event_id = str(uuid.uuid4())
        event_payload = {
            "headers": req.headers.values,
            "body": (await req.body()).decode()
        }
        self.events[event_id] = event_payload
        return Response(f"OK")

    async def get_events(self):
        return self.events

    async def get_event(self, id:str):
        if id not in self.events:
            return Response("NOT FOUND", 404)
        return self.events[id]

    async def delete_event(self, id:str):
        if id not in self.events:
            return Response("NOT FOUND", 404)
        del self.events[id]
        return "OK"

app.include_router(
    WhatsappApplication(TOKEN).register_router(APIRouter()),
    prefix="/whatsapp"
    )

if __name__=="__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True
    )