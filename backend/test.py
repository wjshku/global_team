# Create a test file to demonstrate the backend endpoints
# use requests library, to simulate the requests from the frontend

import requests 

def main():
    base_url = "http://localhost:8000/api/v1"

    # create a new user
    user1_creds = {
        "name": "Test1",
        "email": "test1@example.com",
        "password": "SecurePass123",
        "timezone": "America/New_York"
    }
    user2_creds = {
        "name": "Test2",
        "email": "test2@example.com",
        "password": "SecurePass123",
        "timezone": "America/New_York"
    }
    r = requests.post(f"{base_url}/auth/register", json=user1_creds)
    r = requests.post(f"{base_url}/auth/register", json=user2_creds)

    r = requests.post(f"{base_url}/auth/login", json={"email": user1_creds["email"], "password": user1_creds["password"]})
    user1_token = r.json()["accessToken"]
    assert r.status_code == 200
    r = requests.post(f"{base_url}/auth/login", json={"email": user2_creds["email"], "password": user2_creds["password"]})
    assert r.status_code == 200
    user2_token = r.json()["accessToken"]
    print('Two users created and logged in')

    # get user1 and user2 profiles
    r = requests.get(f"{base_url}/auth/profile", headers={"Authorization": f"Bearer {user1_token}"})
    user1_id = r.json()["id"]
    r = requests.get(f"{base_url}/auth/profile", headers={"Authorization": f"Bearer {user2_token}"})
    user2_id = r.json()["id"]
    print(f'User1 profile: {user1_id}')
    print(f'User2 profile: {user2_id}')

    # user1 create a new team
    team_data = {
        "name": "Test Team",
        "description": "Test Team Description",
        "timezone": "America/New_York"
    }
    r = requests.post(f"{base_url}/teams", json=team_data, headers={"Authorization": f"Bearer {user1_token}"})
    r = requests.get(f'{base_url}/teams', headers={"Authorization": f"Bearer {user1_token}"})
    # Find the team id with the name "Test Team"
    team_id = None
    for team in r.json()['items']:
        if team["name"] == "Test Team":
            team_id = team["id"]
            break
    assert team_id is not None
    r = requests.get(f'{base_url}/teams/{team_id}', json=team_data, headers={"Authorization": f"Bearer {user1_token}"})
    team_id = r.json()["id"]
    print(f'Team created: {team_id}')

    # user1 add user2 to the team
    
    r = requests.post(f'{base_url}/teams/{team_id}/members/{user2_id}', headers={"Authorization": f"Bearer {user1_token}"})
    print(r.json())
    print(f'User2 added to team: {team_id}')

    # user1 create a new meeting
    meeting_data = {
        "title": "Test Meeting",
        "description": "Test Meeting Description",
        "votingStart": "2024-01-15T09:00:00.000Z",
        "votingEnd": "2024-01-22T09:00:00.000Z",
        "timeSlots": ["2024-01-15T09:00:00Z", "2024-01-15T10:00:00Z"],
        "duration": 30,
        "timezone": "America/New_York"
    }
    r = requests.post(f'{base_url}/meetings/team/{team_id}', json=meeting_data, headers={"Authorization": f"Bearer {user1_token}"})
    meeting_id = r.json()["meetId"]
    print(f'Meeting created: {meeting_id}')

    # user1 submit a vote for the meeting
    
    return


if __name__ == "__main__":
    main()