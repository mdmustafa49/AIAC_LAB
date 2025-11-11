from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Simple Search API")

# Example in-memory dataset
class Item(BaseModel):
    id: int
    name: str
    description: str
    tags: List[str] = []

DATA = [
    Item(id=1, name="Red Apple", description="Fresh and crisp apple", tags=["fruit", "food"]),
    Item(id=2, name="Green Apple", description="Sour green apple", tags=["fruit", "food"]),
    Item(id=3, name="Apple MacBook", description="Laptop from Apple", tags=["electronics", "computer"]),
    Item(id=4, name="Banana", description="Yellow banana", tags=["fruit", "food"]),
    Item(id=5, name="Desk Lamp", description="LED lamp for desk", tags=["home", "lighting"]),
]


def match_value(value: str, query: str, exact: bool, case_insensitive: bool) -> bool:
    if case_insensitive:
        value = value.lower()
        query = query.lower()
    return (value == query) if exact else (query in value)


@app.get("/items/search")
def search_items(
    q: Optional[str] = Query(None, description="Query string to search for"),
    fields: Optional[str] = Query("name,description,tags", description="Comma separated fields to search (name,description,tags)"),
    exact: bool = Query(False, description="Match exact values instead of substring"),
    case_insensitive: bool = Query(True, description="Perform case-insensitive matching"),
    limit: int = Query(10, ge=1, le=100, description="Max number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
):
    # Basic validation
    allowed_fields = {"name", "description", "tags"}
    requested = [f.strip() for f in fields.split(",") if f.strip()]
    if not requested:
        raise HTTPException(status_code=400, detail="No fields specified to search")
    if any(f not in allowed_fields for f in requested):
        raise HTTPException(status_code=400, detail=f"Allowed fields: {', '.join(sorted(allowed_fields))}")

    # If no query provided, return empty result set (could also return all)
    if q is None or q == "":
        return {"total": 0, "limit": limit, "offset": offset, "results": []}

    matches = []
    for item in DATA:
        matched = False
        for field in requested:
            if field == "name":
                if match_value(item.name, q, exact, case_insensitive):
                    matched = True
                    break
            elif field == "description":
                if match_value(item.description, q, exact, case_insensitive):
                    matched = True
                    break
            elif field == "tags":
                # tags is a list; check any tag
                for tag in item.tags:
                    if match_value(tag, q, exact, case_insensitive):
                        matched = True
                        break
                if matched:
                    break
        if matched:
            matches.append(item)

    total = len(matches)
    sliced = matches[offset : offset + limit]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": [it.dict() for it in sliced],
    }


if __name__ == "__main__":
    uvicorn.run("task_3:app", host="127.0.0.1", port=8000, reload=True)