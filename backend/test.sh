curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "password": "SecurePass123",
    "timezone": "America/New_York"
  }'

curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'

# Alternatively, login by name:
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "password": "SecurePass123"
  }'

curl -X GET http://localhost:8000/api/v1/teams \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU4NjkzNzc3fQ.-8U6M9erPzyKZQjqdlT7TWVVybMo0ClHUwvJAfp-GoU"


curl -X PUT "http://localhost:8000/api/v1/members/test/availability" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU4NjkzNzc3fQ.-8U6M9erPzyKZQjqdlT7TWVVybMo0ClHUwvJAfp-GoU" \
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

curl -X POST "http://localhost:8000/api/v1/teams" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU4NjkzNzc3fQ.-8U6M9erPzyKZQjqdlT7TWVVybMo0ClHUwvJAfp-GoU" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Team",
    "description": "Team description",
    "timezone": "UTC"
  }'

curl -X POST "http://localhost:8000/api/v1/meetings/team/track-c-6d3c8139" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU4NjkzMTkzfQ.fs19-qer3meAVLIRsAVuoOCKv924h4nhWtLlNqPuen4" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "description": "Daily standup meeting",
    "votingStart": "2024-01-15T09:00:00.000Z",
    "votingEnd": "2024-01-22T09:00:00.000Z",
    "timeSlots": ["2024-01-15T09:00:00Z", "2024-01-15T10:00:00Z"],
    "duration": 30,
    "timezone": "UTC"
  }'


curl -X GET http://localhost:8000/api/v1/members/test/teams \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU4NjkzMTkzfQ.fs19-qer3meAVLIRsAVuoOCKv924h4nhWtLlNqPuen4"