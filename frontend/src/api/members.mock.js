// src/api/mocks/members.mock.js
// Enhanced mock members data with slot-based availability format
// Format: "day_{dayIndex}_slot_{slotIndex}": boolean
// Day indices: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
// Slot indices: 0=8:00-9:00, 1=9:00-10:00, 2=10:00-11:00, etc. (60-minute intervals)
export const MOCK_MEMBERS = [
  {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    timezone: 'America/New_York',
    role: 'admin',
    status: 'online',
    availability: {
      // Monday (day_0) - 9 AM to 5 PM (slots 1-9)
      "day_0_slot_9": true, "day_0_slot_10": true, "day_0_slot_11": true,
      "day_0_slot_12": true, "day_0_slot_13": true, "day_0_slot_14": true,
      "day_0_slot_15": true, "day_0_slot_16": true, "day_0_slot_17": true,
      
      // Tuesday (day_1) - 9 AM to 5 PM
      "day_1_slot_9": true, "day_1_slot_10": true, "day_1_slot_11": true,
      "day_1_slot_12": true, "day_1_slot_13": true, "day_1_slot_14": true,
      "day_1_slot_15": true, "day_1_slot_16": true, "day_1_slot_17": true,
  
      // Wednesday (day_2) - 9 AM to 5 PM
      "day_2_slot_9": true, "day_2_slot_10": true, "day_2_slot_11": true,
      "day_2_slot_12": true, "day_2_slot_13": true, "day_2_slot_14": true,
      "day_2_slot_15": true, "day_2_slot_16": true, "day_2_slot_17": true,

      // Thursday (day_3) - 9 AM to 5 PM
      "day_3_slot_9": true, "day_3_slot_10": true, "day_3_slot_11": true,
      "day_3_slot_12": true, "day_3_slot_13": true, "day_3_slot_14": true,
      "day_3_slot_15": true, "day_3_slot_16": true, "day_3_slot_17": true,
      
    },
    teams: ['1', '2'],
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
    createdAt: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    timezone: 'Asia/Singapore',
    role: 'member',
    status: 'away',
    availability: {
      // Monday (day_0) - 8 AM to 4 PM (slots 0-8)
      "day_0_slot_8": true, "day_0_slot_9": true, "day_0_slot_10": true,
      "day_0_slot_11": true, "day_0_slot_12": true, "day_0_slot_13": true,
      "day_0_slot_14": true, "day_0_slot_15": true, "day_0_slot_16": true,
      
      // Tuesday (day_1) - 8 AM to 4 PM
      "day_1_slot_8": true, "day_1_slot_9": true, "day_1_slot_10": true,
      "day_1_slot_11": true, "day_1_slot_12": true, "day_1_slot_13": true,
      "day_1_slot_14": true, "day_1_slot_15": true, "day_1_slot_16": true,

      // Wednesday (day_2) - 8 AM to 4 PM
      "day_2_slot_8": true, "day_2_slot_9": true, "day_2_slot_10": true,
      "day_2_slot_11": true, "day_2_slot_12": true, "day_2_slot_13": true,
      "day_2_slot_14": true, "day_2_slot_15": true, "day_2_slot_16": true,

      // Thursday (day_3) - 8 AM to 4 PM
      "day_3_slot_8": true, "day_3_slot_9": true, "day_3_slot_10": true,
      "day_3_slot_11": true, "day_3_slot_12": true, "day_3_slot_13": true,
      "day_3_slot_14": true, "day_3_slot_15": true, "day_3_slot_16": true,

      // Friday (day_4) - 8 AM to 2 PM (slots 0-6)
      "day_4_slot_8": true, "day_4_slot_9": true, "day_4_slot_10": true,
      "day_4_slot_11": true, "day_4_slot_12": true, "day_4_slot_13": true,
      "day_4_slot_14": true, "day_4_slot_15": true, "day_4_slot_16": true,

    },
    teams: ['1', '3'],
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
    createdAt: '2024-01-16T14:30:00Z'
  },
  {
    id: '3',
    name: 'Mike Johnson',
    email: 'mike@example.com',
    timezone: 'Asia/Singapore',
    role: 'member',
    status: 'offline',
    availability: {
      // Monday (day_0) - 10 AM to 6 PM (slots 2-10)
      "day_0_slot_2": true, "day_0_slot_3": true, "day_0_slot_4": true,
      "day_0_slot_5": true, "day_0_slot_6": true, "day_0_slot_7": true,
      "day_0_slot_8": true, "day_0_slot_9": true, "day_0_slot_10": true,
      
      // Tuesday (day_1) - 10 AM to 6 PM
      "day_1_slot_2": true, "day_1_slot_3": true, "day_1_slot_4": true,
      "day_1_slot_5": true, "day_1_slot_6": true, "day_1_slot_7": true,
      "day_1_slot_8": true, "day_1_slot_9": true, "day_1_slot_10": true,
      
      // Wednesday (day_2) - 10 AM to 6 PM
      "day_2_slot_2": true, "day_2_slot_3": true, "day_2_slot_4": true,
      "day_2_slot_5": true, "day_2_slot_6": true, "day_2_slot_7": true,
      "day_2_slot_8": true, "day_2_slot_9": true, "day_2_slot_10": true,
      
      // Thursday (day_3) - 10 AM to 6 PM
      "day_3_slot_2": true, "day_3_slot_3": true, "day_3_slot_4": true,
      "day_3_slot_5": true, "day_3_slot_6": true, "day_3_slot_7": true,
      "day_3_slot_8": true, "day_3_slot_9": true, "day_3_slot_10": true,
      
      // Friday (day_4) - 10 AM to 4 PM (slots 2-8)
      "day_4_slot_2": true, "day_4_slot_3": true, "day_4_slot_4": true,
      "day_4_slot_5": true, "day_4_slot_6": true, "day_4_slot_7": true,
      "day_4_slot_8": true
    },
    teams: ['2', '3'],
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mike',
    createdAt: '2024-01-17T09:15:00Z'
  },
  {
    id: '4',
    name: 'Sarah Wilson',
    email: 'sarah@example.com',
    timezone: 'America/New_York',
    role: 'member',
    status: 'busy',
    availability: {
      // Monday (day_0) - 9:30 AM to 5:30 PM (slots 1.5-9.5, rounded to 1-10)
      "day_0_slot_1": true, "day_0_slot_2": true, "day_0_slot_3": true,
      "day_0_slot_4": true, "day_0_slot_5": true, "day_0_slot_6": true,
      "day_0_slot_7": true, "day_0_slot_8": true, "day_0_slot_9": true,
      "day_0_slot_10": true,
      
      // Tuesday (day_1) - 9:30 AM to 5:30 PM
      "day_1_slot_1": true, "day_1_slot_2": true, "day_1_slot_3": true,
      "day_1_slot_4": true, "day_1_slot_5": true, "day_1_slot_6": true,
      "day_1_slot_7": true, "day_1_slot_8": true, "day_1_slot_9": true,
      "day_1_slot_10": true,
      
      // Wednesday (day_2) - 9:30 AM to 5:30 PM
      "day_2_slot_1": true, "day_2_slot_2": true, "day_2_slot_3": true,
      "day_2_slot_4": true, "day_2_slot_5": true, "day_2_slot_6": true,
      "day_2_slot_7": true, "day_2_slot_8": true, "day_2_slot_9": true,
      "day_2_slot_10": true,
      
      // Thursday (day_3) - 9:30 AM to 5:30 PM
      "day_3_slot_1": true, "day_3_slot_2": true, "day_3_slot_3": true,
      "day_3_slot_4": true, "day_3_slot_5": true, "day_3_slot_6": true,
      "day_3_slot_7": true, "day_3_slot_8": true, "day_3_slot_9": true,
      "day_3_slot_10": true,
      
      // Friday (day_4) - 9:30 AM to 3:30 PM (slots 1-7)
      "day_4_slot_1": true, "day_4_slot_2": true, "day_4_slot_3": true,
      "day_4_slot_4": true, "day_4_slot_5": true, "day_4_slot_6": true,
      "day_4_slot_7": true
    },
    teams: ['1', '2', '3'],
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
    createdAt: '2024-01-18T16:45:00Z'
  }
]
  
  export async function fetchMembersMock() {
    await new Promise(r => setTimeout(r, 100));
    return MOCK_MEMBERS;
  }
  
  export async function updateMemberMock(memberId, updates) {
    await new Promise(r => setTimeout(r, 200));
    const idx = MOCK_MEMBERS.findIndex(m => m.id === memberId);
    if (idx !== -1) {
      MOCK_MEMBERS[idx] = { ...MOCK_MEMBERS[idx], ...updates };
      return MOCK_MEMBERS[idx];
    }
    throw new Error('Member not found');
  }
  
  export async function updateAvailabilityMock(memberId, availability) {
    await new Promise(r => setTimeout(r, 100));
    const member = MOCK_MEMBERS.find(m => m.id === memberId);
    if (!member) throw new Error('Member not found');
    member.availability = availability;
    return member;
  }