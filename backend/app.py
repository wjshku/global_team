from __future__ import annotations
import os

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Literal, Optional, TypedDict, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

try:
    from zoneinfo import ZoneInfo, available_timezones  # Python 3.9+
except Exception:  # pragma: no cover
    # Fallback for environments without zoneinfo; not expected on modern Python
    ZoneInfo = None  # type: ignore
    available_timezones = lambda: set()  # type: ignore


# Resolve directories relative to the global_team package root
GLOBAL_TEAM_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = GLOBAL_TEAM_DIR / "backend"
FRONTEND_DIR = GLOBAL_TEAM_DIR / "frontend"
FRONTEND_DIST = FRONTEND_DIR / "dist"
DATA_DIR = BACKEND_DIR / "data"
DATA_FILE = DATA_DIR / "members.json"
TEAMS_FILE = DATA_DIR / "teams.json"


class Member(TypedDict, total=False):
    name: str
    timezone: str
    availability: List[int]  # 24-length array of 0/1 indicating availability per UTC hour


class AddMemberPayload(BaseModel):
    action: Literal["add_member"]
    name: str = Field(..., min_length=1, max_length=100)
    timezone: str = Field(..., min_length=1, max_length=100)


class ListMembersPayload(BaseModel):
    action: Literal["list_members"]


class ProposeMeetingPayload(BaseModel):
    action: Literal["propose_meeting"]
    utc_datetime: str = Field(..., description="ISO 8601 UTC datetime, e.g., 2025-09-16T15:00:00Z")


class ProposeMeetingLocalPayload(BaseModel):
    action: Literal["propose_meeting_local"]
    date: str = Field(..., description="Local date YYYY-MM-DD")
    time: str = Field(..., description="Local time HH:MM (24h)")
    timezone: str = Field(..., min_length=1, max_length=100)


class ListTeamsPayload(BaseModel):
    action: Literal["list_teams"]


class CreateTeamPayload(BaseModel):
    action: Literal["create_team"]
    name: str = Field(..., min_length=1, max_length=100)
    creator_name: Optional[str] = Field(None, max_length=100)
    creator_timezone: Optional[str] = Field(None, max_length=100)


class AddMemberToTeamPayload(BaseModel):
    action: Literal["add_member_to_team"]
    team: str = Field(..., min_length=1, max_length=100)
    member_name: str = Field(..., min_length=1, max_length=100)


class GetTeamPayload(BaseModel):
    action: Literal["get_team"]
    team: str = Field(..., min_length=1, max_length=100)
    requester_name: str = Field(..., min_length=1, max_length=100)


class JoinTeamPayload(BaseModel):
    action: Literal["join_team"]
    team: str = Field(..., min_length=1, max_length=100)
    member_name: str = Field(..., min_length=1, max_length=100)


class ListTimezonesPayload(BaseModel):
    action: Literal["list_timezones"]


class GetMemberPayload(BaseModel):
    action: Literal["get_member"]
    name: str = Field(..., min_length=1, max_length=100)


class UpdateMemberTimezonePayload(BaseModel):
    action: Literal["update_member_timezone"]
    name: str = Field(..., min_length=1, max_length=100)
    timezone: str = Field(..., min_length=1, max_length=100)


class UpdateAvailabilityPayload(BaseModel):
    action: Literal["update_availability"]
    name: str = Field(..., min_length=1, max_length=100)
    availability: List[int] = Field(..., description="24-length list with 0/1 values per UTC hour")


ActionPayload = (
    AddMemberPayload
    | ListMembersPayload
    | ProposeMeetingPayload
    | ProposeMeetingLocalPayload
    | ListTeamsPayload
    | CreateTeamPayload
    | AddMemberToTeamPayload
    | GetTeamPayload
    | JoinTeamPayload
    | ListTimezonesPayload
    | GetMemberPayload
    | UpdateMemberTimezonePayload
    | UpdateAvailabilityPayload
)


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    if not TEAMS_FILE.exists():
        TEAMS_FILE.write_text("{}", encoding="utf-8")


def read_members() -> List[Member]:
    ensure_storage()
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            valid_members: List[Member] = []
            for item in data:
                if isinstance(item, dict) and "name" in item and "timezone" in item:
                    availability: List[int]
                    if isinstance(item.get("availability"), list) and len(item.get("availability")) == 24:
                        # sanitize values to 0/1 ints
                        availability = [1 if int(v) else 0 for v in item.get("availability")]  # type: ignore[arg-type]
                    else:
                        # default to business hours 09:00-17:00 UTC
                        availability = [1 if 9 <= h < 17 else 0 for h in range(24)]
                    valid_members.append({
                        "name": str(item["name"]),
                        "timezone": str(item["timezone"]),
                        "availability": availability,
                    })
            return valid_members
        return []
    except json.JSONDecodeError:
        return []


def write_members(members: List[Member]) -> None:
    ensure_storage()
    DATA_FILE.write_text(json.dumps(members, ensure_ascii=False, indent=2), encoding="utf-8")


def read_teams() -> Dict[str, List[str]]:
    ensure_storage()
    try:
        data = json.loads(TEAMS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            normalized: Dict[str, List[str]] = {}
            for team_name, members in data.items():
                if isinstance(team_name, str) and isinstance(members, list):
                    normalized[team_name] = [str(m) for m in members]
            return normalized
        return {}
    except json.JSONDecodeError:
        return {}


def write_teams(teams: Dict[str, List[str]]) -> None:
    ensure_storage()
    TEAMS_FILE.write_text(json.dumps(teams, ensure_ascii=False, indent=2), encoding="utf-8")


def is_valid_timezone(tz: str) -> bool:
    try:
        return tz in available_timezones()
    except Exception:
        # If available_timezones is unavailable, attempt constructing ZoneInfo
        try:
            ZoneInfo(tz)  # type: ignore[call-arg]
            return True
        except Exception:
            return False


def parse_utc_datetime(dt_str: str) -> datetime:
    # Accept forms like 2025-09-16T15:00:00Z or with +00:00
    try:
        if dt_str.endswith("Z"):
            dt_str = dt_str[:-1] + "+00:00"
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            # Treat naive as UTC
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid utc_datetime. Use ISO 8601, e.g., 2025-09-16T15:00:00Z")


def parse_local_to_utc(date_str: str, time_str: str, tz_name: str) -> datetime:
    try:
        if ZoneInfo is None:
            raise ValueError("ZoneInfo unavailable")
        # Basic validation
        yyyy, mm, dd = [int(x) for x in date_str.split("-")]
        hh, mi = [int(x) for x in time_str.split(":")]
        local = datetime(yyyy, mm, dd, hh, mi, 0, tzinfo=ZoneInfo(tz_name))  # type: ignore[call-arg]
        return local.astimezone(timezone.utc)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid local date/time/timezone")


app = FastAPI(title="Global Team Manager", version="0.1.0")

# Enable permissive CORS by default; tighten origins via env FRONTEND_ORIGIN if desired
frontend_origin = os.environ.get("FRONTEND_ORIGIN")
allow_origins = [frontend_origin] if frontend_origin else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve built Vue assets at /assets if available
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/app", status_code=307)


@app.get("/favicon.ico")
def favicon():
    # Empty 204 to suppress favicon 404 logs
    return Response(status_code=204)


@app.get("/app")
def get_app(asset: Optional[str] = None):
    # Serve the frontend or small assets via a single endpoint
    if asset == "css":
        css_file = FRONTEND_DIR / "css" / "style.css"
        if css_file.exists():
            return PlainTextResponse(css_file.read_text(encoding="utf-8"), media_type="text/css")
        return PlainTextResponse(":root{color-scheme:light dark}", media_type="text/css")

    if asset == "js":
        js_file = FRONTEND_DIR / "js" / "app.js"
        if js_file.exists():
            return PlainTextResponse(js_file.read_text(encoding="utf-8"), media_type="application/javascript")
        return PlainTextResponse("console.warn('No JS found');", media_type="application/javascript")

    # Prefer built Vue app if present
    index_file = FRONTEND_DIST / "index.html"
    if not index_file.exists():
        index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=500, detail="Frontend not found")
    html = index_file.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.post("/app")
async def post_app(request: Request) -> JSONResponse:
    payload = await request.json()

    action: Optional[str] = payload.get("action") if isinstance(payload, dict) else None
    if action is None:
        raise HTTPException(status_code=400, detail="Missing 'action'")

    if action == "list_members":
        members = read_members()
        return JSONResponse({"ok": True, "members": members})

    if action == "list_timezones":
        try:
            tzs = sorted(list(available_timezones()))
        except Exception:
            tzs = []
        return JSONResponse({"ok": True, "timezones": tzs})

    if action == "add_member":
        try:
            parsed = AddMemberPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        if not is_valid_timezone(parsed.timezone):
            raise HTTPException(status_code=400, detail="Invalid timezone")

        members = read_members()
        # prevent duplicates by name (case-insensitive)
        if any(m["name"].strip().lower() == parsed.name.strip().lower() for m in members):
            return JSONResponse({"ok": False, "error": "Member with this name already exists"}, status_code=400)

        # default availability 09:00-17:00 UTC
        default_availability = [1 if 9 <= h < 17 else 0 for h in range(24)]
        members.append({"name": parsed.name.strip(), "timezone": parsed.timezone, "availability": default_availability})
        write_members(members)
        return JSONResponse({"ok": True, "members": members})

    if action == "list_teams":
        teams = read_teams()
        # respond with team names and counts
        items = [{"name": k, "member_count": len(v)} for k, v in sorted(teams.items())]
        return JSONResponse({"ok": True, "teams": items})

    if action == "create_team":
        try:
            parsed = CreateTeamPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        teams = read_teams()
        if parsed.name in teams:
            return JSONResponse({"ok": False, "error": "Team already exists"}, status_code=400)
        teams[parsed.name] = []
        # Auto-add creator if provided; optionally create member if timezone is provided
        if parsed.creator_name:
            members = read_members()
            if not any(m["name"].strip().lower() == parsed.creator_name.strip().lower() for m in members):
                if parsed.creator_timezone:
                    if not is_valid_timezone(parsed.creator_timezone):
                        raise HTTPException(status_code=400, detail="Invalid creator_timezone")
                    members.append({"name": parsed.creator_name.strip(), "timezone": parsed.creator_timezone})
                    write_members(members)
                else:
                    return JSONResponse({"ok": False, "error": "Creator not a member. Provide creator_timezone to auto-create."}, status_code=400)
            if parsed.creator_name not in teams[parsed.name]:
                teams[parsed.name].append(parsed.creator_name)
        write_teams(teams)
        return JSONResponse({"ok": True, "team": {"name": parsed.name, "member_count": len(teams[parsed.name])}})

    if action == "add_member_to_team":
        try:
            parsed = AddMemberToTeamPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        teams = read_teams()
        if parsed.team not in teams:
            return JSONResponse({"ok": False, "error": "Team not found"}, status_code=404)
        members = read_members()
        if not any(m["name"].strip().lower() == parsed.member_name.strip().lower() for m in members):
            return JSONResponse({"ok": False, "error": "Member not found"}, status_code=404)
        team_members = teams[parsed.team]
        if parsed.member_name not in team_members:
            team_members.append(parsed.member_name)
            write_teams(teams)
        return JSONResponse({"ok": True, "team": parsed.team, "members": team_members})

    if action == "get_team":
        try:
            parsed = GetTeamPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        teams = read_teams()
        if parsed.team not in teams:
            return JSONResponse({"ok": False, "error": "Team not found"}, status_code=404)
        team_members = teams[parsed.team]
        # membership gate
        if parsed.requester_name not in team_members:
            return JSONResponse({"ok": False, "error": "Forbidden: not a team member"}, status_code=403)
        # return member list with timezone and availability
        all_members_list = read_members()
        all_members: Dict[str, Member] = {m["name"]: m for m in all_members_list}
        team_detail = []
        for name in team_members:
            member = all_members.get(name)
            if member is None:
                team_detail.append({"name": name, "timezone": None, "availability": [0]*24})
            else:
                team_detail.append({
                    "name": member["name"],
                    "timezone": member.get("timezone"),
                    "availability": member.get("availability", [0]*24),
                })
        return JSONResponse({"ok": True, "team": parsed.team, "members": team_detail})

    if action == "join_team":
        try:
            parsed = JoinTeamPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        teams = read_teams()
        if parsed.team not in teams:
            return JSONResponse({"ok": False, "error": "Team not found"}, status_code=404)
        members = read_members()
        if not any(m["name"].strip().lower() == parsed.member_name.strip().lower() for m in members):
            return JSONResponse({"ok": False, "error": "Member not found"}, status_code=404)
        if parsed.member_name not in teams[parsed.team]:
            teams[parsed.team].append(parsed.member_name)
            write_teams(teams)
        return JSONResponse({"ok": True, "team": parsed.team, "members": teams[parsed.team]})

    if action == "propose_meeting":
        try:
            parsed = ProposeMeetingPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        utc_dt = parse_utc_datetime(parsed.utc_datetime)
        members = read_members()
        schedule = []
        for m in members:
            try:
                local_dt = utc_dt.astimezone(ZoneInfo(m["timezone"]))  # type: ignore[arg-type]
                schedule.append(
                    {
                        "name": m["name"],
                        "timezone": m["timezone"],
                        "local_datetime": local_dt.isoformat(),
                        "weekday": local_dt.strftime("%A"),
                    }
                )
            except Exception:
                schedule.append(
                    {
                        "name": m["name"],
                        "timezone": m["timezone"],
                        "error": "Invalid timezone",
                    }
                )
        return JSONResponse({"ok": True, "utc_datetime": utc_dt.isoformat(), "schedule": schedule})

    if action == "propose_meeting_local":
        try:
            parsed = ProposeMeetingLocalPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        if not is_valid_timezone(parsed.timezone):
            raise HTTPException(status_code=400, detail="Invalid timezone")
        utc_dt = parse_local_to_utc(parsed.date, parsed.time, parsed.timezone)
        members = read_members()
        schedule = []
        for m in members:
            try:
                local_dt = utc_dt.astimezone(ZoneInfo(m["timezone"]))  # type: ignore[arg-type]
                schedule.append(
                    {
                        "name": m["name"],
                        "timezone": m["timezone"],
                        "local_datetime": local_dt.isoformat(),
                        "weekday": local_dt.strftime("%A"),
                    }
                )
            except Exception:
                schedule.append(
                    {
                        "name": m["name"],
                        "timezone": m["timezone"],
                        "error": "Invalid timezone",
                    }
                )
        return JSONResponse({"ok": True, "utc_datetime": utc_dt.isoformat(), "schedule": schedule})

    if action == "get_member":
        try:
            parsed = GetMemberPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        members = read_members()
        for m in members:
            if m["name"].strip().lower() == parsed.name.strip().lower():
                return JSONResponse({"ok": True, "member": m})
        return JSONResponse({"ok": False, "error": "Member not found"}, status_code=404)

    if action == "update_member_timezone":
        try:
            parsed = UpdateMemberTimezonePayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        if not is_valid_timezone(parsed.timezone):
            raise HTTPException(status_code=400, detail="Invalid timezone")
        members = read_members()
        updated = False
        for m in members:
            if m["name"].strip().lower() == parsed.name.strip().lower():
                m["timezone"] = parsed.timezone
                updated = True
                break
        if not updated:
            return JSONResponse({"ok": False, "error": "Member not found"}, status_code=404)
        write_members(members)
        return JSONResponse({"ok": True})

    if action == "update_availability":
        try:
            parsed = UpdateAvailabilityPayload(**payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        if not isinstance(parsed.availability, list) or len(parsed.availability) != 24:
            raise HTTPException(status_code=400, detail="availability must be 24-length list of 0/1")
        sanitized = []
        try:
            for v in parsed.availability:
                sanitized.append(1 if int(v) else 0)
        except Exception:
            raise HTTPException(status_code=400, detail="availability must contain integers 0 or 1")
        members = read_members()
        updated = False
        for m in members:
            if m["name"].strip().lower() == parsed.name.strip().lower():
                m["availability"] = sanitized
                updated = True
                break
        if not updated:
            return JSONResponse({"ok": False, "error": "Member not found"}, status_code=404)
        write_members(members)
        return JSONResponse({"ok": True})

    raise HTTPException(status_code=400, detail="Unknown action")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


