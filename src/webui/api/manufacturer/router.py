from fastapi import APIRouter, Query, HTTPException
from starlette.responses import HTMLResponse

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.logger_provider import logger

manufacturer_router = APIRouter(tags=['api'], prefix=f"{settings.base_url}/manufacturer")


@manufacturer_router.get("/search/", response_class=HTMLResponse)
async def type_search(q: str = Query(default=None, min_length=3, max_length=50, description="Search query")):
    if q is None or q.strip() == "":
        return HTMLResponse(
            content="<div id='results'><div class='p-2'>Please provide a search criteria.</div></div>",
            status_code=400)

    try:
        query = f"FOR doc IN manufacturer FILTER LIKE(doc.name, @query, true) RETURN doc"
        bind_vars = {"query": f"%{q}%"}
        db = ArangoDBConnection.get_instance().get_connection()
        cursor = db.aql.execute(query, bind_vars=bind_vars)
        results = [doc for doc in cursor]

        if not results:
            return HTMLResponse(
                content="<div id='results'><div class='p-2'>No results found.</div></div>",
                status_code=404)

        results_html = "".join([f"<option value='{doc['name']}'></option>" for doc in results])
        return HTMLResponse(content=results_html, status_code=200)

    except Exception as e:
        # Log the error details here using logging if needed
        logger.error(f"An error occurred while querying Manufacturer: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while querying the database.")
