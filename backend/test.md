### API I/O Examples (based on backend/test.py and backend/test.sh)

All endpoints are under base URL: `http://localhost:8000/api/v1`

Authentication uses Bearer JWT in the `Authorization` header: `Authorization: Bearer <token>`.

---

### Auth: Register

Request
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test1",
    "email": "test1@example.com",
    "password": "SecurePass123",
    "timezone": "America/New_York"
  }'
```

Response (201)
```json
{
  "user": {
    "id": "usr_12345",
    "name": "Test1",
    "email": "test1@example.com",
    "timezone": "America/New_York",
    "role": "member",
    "avatar": "https://ui-avatars.com/api/?name=T&background=1a2b3c&color=fff&size=128&bold=true",
    "createdAt": "2024-01-15T09:00:00Z"
  },
  "token": {
    "accessToken": "<JWT>",
    "tokenType": "bearer"
  }
}
```

---

### Auth: Login (by email)

Request
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test1@example.com",
    "password": "SecurePass123"
  }'
```

Response (200)
```json
{
  "accessToken": "<JWT>",
  "tokenType": "bearer"
}
```

### Auth: Login (by name)

Request
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test1",
    "password": "SecurePass123"
  }'
```

Response (200)
```json
{
  "accessToken": "<JWT>",
  "tokenType": "bearer"
}
```

---

### Auth: Get Profile

Request
```bash
curl -X GET "http://localhost:8000/api/v1/auth/profile" \
  -H "Authorization: Bearer <JWT>"
```

Response (200)
```json
{
  "id": "usr_12345",
  "name": "Test1",
  "email": "test1@example.com",
  "timezone": "America/New_York",
  "role": "member",
  "avatar": "https://ui-avatars.com/api/?name=T&background=1a2b3c&color=fff&size=128&bold=true",
  "createdAt": "2024-01-15T09:00:00Z"
}
```

---

### Teams: List Teams

Request
```bash
curl -X GET "http://localhost:8000/api/v1/teams" \
  -H "Authorization: Bearer <JWT>"
```

Response (200)
```json
{
  "items": [
    {
      "id": "team_abc",
      "name": "Test Team",
      "description": "Test Team Description",
      "timezone": "America/New_York",
      "members": ["usr_12345"],
      "admin": "usr_12345",
      "memberCount": 1,
      "meetingCount": 0,
      "createdAt": "2024-01-15T09:05:00Z"
    }
  ]
}
```

---

### Teams: Create Team

Request
```bash
curl -X POST "http://localhost:8000/api/v1/teams" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Team",
    "description": "Test Team Description",
    "timezone": "America/New_York"
  }'
```

Response (201)
```json
{
  "id": "team_abc",
  "name": "Test Team",
  "description": "Test Team Description",
  "timezone": "America/New_York",
  "members": ["usr_12345"],
  "admin": "usr_12345",
  "memberCount": 1,
  "meetingCount": 0,
  "createdAt": "2024-01-15T09:05:00Z"
}
```

---

### Teams: Get Team by ID

Request
```bash
curl -X GET "http://localhost:8000/api/v1/teams/team_abc" \
  -H "Authorization: Bearer <JWT>"
```

Response (200)
```json
{
  "id": "team_abc",
  "name": "Test Team",
  "description": "Test Team Description",
  "timezone": "America/New_York",
  "members": ["usr_12345", "usr_67890"],
  "admin": "usr_12345",
  "memberCount": 2,
  "meetingCount": 1,
  "createdAt": "2024-01-15T09:05:00Z"
}
```

---

### Teams: Add Member to Team

Request
```bash
curl -X POST "http://localhost:8000/api/v1/teams/team_abc/members/usr_67890" \
  -H "Authorization: Bearer <JWT>"
```

Response (200)
```json
{
  "id": "team_abc",
  "name": "Test Team",
  "description": "Test Team Description",
  "timezone": "America/New_York",
  "members": ["usr_12345", "usr_67890"],
  "admin": "usr_12345",
  "memberCount": 2,
  "meetingCount": 1,
  "createdAt": "2024-01-15T09:05:00Z"
}
```

---

### Members: Update Availability

Request
```bash
curl -X PUT "http://localhost:8000/api/v1/members/usr_12345/availability" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{
    "availability": {
      "day_0_slot_9": true,
      "day_0_slot_10": true,
      "day_0_slot_11": false,
      "day_1_slot_14": true,
      "day_1_slot_15": true,
      "day_2_slot_9": false,
      "day_2_slot_10": true
    }
  }'
```

Response (200)
```json
{
  "id": "usr_12345",
  "name": "Test1",
  "email": "test1@example.com",
  "timezone": "America/New_York",
  "role": "member",
  "status": "active",
  "availability": {
    "day_0_slot_9": true,
    "day_0_slot_10": true,
    "day_0_slot_11": false,
    "day_1_slot_14": true,
    "day_1_slot_15": true,
    "day_2_slot_9": false,
    "day_2_slot_10": true
  },
  "teams": ["team_abc"],
  "avatar": "https://ui-avatars.com/api/?name=T&background=1a2b3c&color=fff&size=128&bold=true",
  "createdAt": "2024-01-15T09:00:00Z"
}
```

---

### Members: Get Member Teams

Request
```bash
curl -X GET "http://localhost:8000/api/v1/members/usr_12345/teams" \
  -H "Authorization: Bearer <JWT>"
```

Response (200)
```json
{
  "items": ["team_abc", "team_xyz"]
}
```

---

### Meetings: Create Meeting for a Team

Request
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/team/team_abc" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Meeting",
    "description": "Test Meeting Description",
    "votingStart": "2024-01-15T09:00:00.000Z",
    "votingEnd": "2024-01-22T09:00:00.000Z",
    "timeSlots": [
      "2024-01-15T09:00:00Z",
      "2024-01-15T10:00:00Z"
    ],
    "duration": 30,
    "timezone": "America/New_York"
  }'
```

Response (201)
```json
{
  "meetId": "meet_123",
  "title": "Test Meeting",
  "description": "Test Meeting Description",
  "teamId": "team_abc",
  "timeSlots": [
    "2024-01-15T09:00:00Z",
    "2024-01-15T10:00:00Z"
  ],
  "scheduledTime": null,
  "votingStart": "2024-01-15T09:00:00.000Z",
  "votingEnd": "2024-01-22T09:00:00.000Z",
  "duration": 30,
  "timezone": "America/New_York",
  "status": "draft",
  "createdAt": "2024-01-15T09:10:00Z"
}
```

---

### Meetings: Submit Vote (optional)

Request
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/meet_123/votes" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "usr_12345",
    "timeSlot": "2024-01-15T10:00:00Z",
    "preference": "high"
  }'
```

Response (200)
```json
{
  "id": "vote_567",
  "meetId": "meet_123",
  "userId": "usr_12345",
  "timeSlot": "2024-01-15T10:00:00Z",
  "preference": "high",
  "createdAt": "2024-01-15T09:12:00Z"
}
```

---

Notes
- IDs and timestamps above are examples. Actual values are generated by the server.
- Login accepts exactly one of "email" or "name" with "password".
- Users are assigned a default `avatar` URL at registration based on their name (UI Avatars style).
- Many team endpoints return the full `TeamResponse`, which includes `memberCount` and `meetingCount` derived fields.
