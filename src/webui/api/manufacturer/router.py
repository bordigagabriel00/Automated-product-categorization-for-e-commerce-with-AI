from fastapi import APIRouter, Query
from starlette.responses import HTMLResponse

from config import settings
from core.arangodb_provider import ArangoDBConnection

manufacturer_router = APIRouter(tags=['api'], prefix=f"{settings.base_url}/manufacturer")


@manufacturer_router.get("/search/")
async def type_search(q: str = Query(default=None)):
    if q is None:
        return HTMLResponse(
            content="<div id='results'><div class='p-2'>Without criteria</div></div>",
            status_code=200)

    query = f"FOR doc IN types FILTER LIKE(doc.name, '%{q}%', true) RETURN doc"
    db = ArangoDBConnection.get_instance().get_connection()
    cursor = db.aql.execute(query)
    results = [doc for doc in cursor]

    results_html = "".join([f"<option value='{doc['name']}'></option>"for doc in results])

    return HTMLResponse(content=results_html, status_code=200)
