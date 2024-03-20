from arango.exceptions import ArangoError
from fastapi import APIRouter, Query, HTTPException
from starlette.responses import HTMLResponse

from config import settings
from core.arangodb_provider import ArangoDBConnection

product_type_router = APIRouter(tags=['api'], prefix=f"{settings.base_url}/type")


@product_type_router.get("/search/", response_class=HTMLResponse)
async def type_search(
        q: str = Query(default=None, min_length=1, max_length=50, description="Search query for product types")):
    if q is None or q.strip() == "":
        return HTMLResponse(
            content="<div id='results'><div class='p-2'>Please provide a search criteria.</div></div>",
            status_code=400)

    try:
        query = f"FOR doc IN product_type FILTER LIKE(doc.name, @query, true) RETURN doc"
        bind_vars = {"query": f"%{q}%"}
        db = ArangoDBConnection.get_instance().get_connection()
        cursor = db.aql.execute(query, bind_vars=bind_vars)
        results = [doc for doc in cursor]

        if not results:
            return HTMLResponse(
                content="<div id='results'><div class='p-2'>No results found for your query.</div></div>",
                status_code=404)

        results_html = "".join([f"<option value='{doc['name']}'></option>" for doc in results])
        return HTMLResponse(content=results_html, status_code=200)

    except ArangoError as e:
        # Log the error here for debugging
        logger.error(f"An error occurred while querying product type: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while querying the database.")
