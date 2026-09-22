from fastapi import FastAPI
import inngest as ig
import inngest.fast_api
import logging



app = FastAPI()
client = ig.Inngest(
    app_id="flyrank",
    logger=logging.getLogger("uvicorn"),
    is_production=False,  # dev mode — no signing key needed; set True + INNGEST_SIGNING_KEY in prod
)

@client.create_function(fn_id="say_hello",trigger=ig.TriggerEvent(event="test/hello"))
async def say_hello(ctx : ig.Context) -> dict[str,str]:
    ctx.logger.info(f"event: {ctx.event}")
    await ctx.step.sleep("wait-5s", "5s")
    return {"message": "Hello from background"}


# Expose /api/inngest for Inngest to discover & invoke functions
import inngest.fast_api as _inngest_fast_api

_inngest_fast_api.serve(app, client, [say_hello])


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)