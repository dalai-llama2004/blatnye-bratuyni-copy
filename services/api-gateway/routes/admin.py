from fastapi import APIRouter, Request, Depends, Response
import requests
from config import BOOKING_SERVICE_URL
from auth import get_current_user

router = APIRouter()

@router.post("/zones")
async def create_zone(request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = {
        "X-User-Id": str(user.get('user_id', user.get('sub'))),
        "X-User-Role": user.get('role', 'user')
    }
    resp = requests.post(f"{BOOKING_SERVICE_URL}/admin/zones", json=body, headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type',"application/json"))

@router.patch("/zones/{zone_id}")
async def update_zone(zone_id: int, request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = {
        "X-User-Id": str(user.get('user_id', user.get('sub'))),
        "X-User-Role": user.get('role', 'user')
    }
    resp = requests.patch(f"{BOOKING_SERVICE_URL}/admin/zones/{zone_id}", json=body, headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type',"application/json"))

@router.delete("/zones/{zone_id}")
async def delete_zone(zone_id: int, user=Depends(get_current_user)):
    headers = {
        "X-User-Id": str(user.get('user_id', user.get('sub'))),
        "X-User-Role": user.get('role', 'user')
    }
    resp = requests.delete(f"{BOOKING_SERVICE_URL}/admin/zones/{zone_id}", headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type',"application/json"))

@router.post("/zones/{zone_id}/close")
async def close_zone(zone_id: int, request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = {
        "X-User-Id": str(user.get('user_id', user.get('sub'))),
        "X-User-Role": user.get('role', 'user')
    }
    resp = requests.post(f"{BOOKING_SERVICE_URL}/admin/zones/{zone_id}/close", json=body, headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type',"application/json"))
