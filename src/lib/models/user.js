// User model shape
export const UserModel = {
  uid: '',
  firstName: '',
  lastName: '',
  email: '',
  dateJoined: '', // ISO string
  skills: [], // Array of strings
  teams: [], // Array of team IDs
  isAdmin: false
};

export function createUser(uid, firstName, lastName, email) {
  return {
    uid,
    firstName,
    lastName,
    email,
    dateJoined: new Date().toISOString(),
    skills: [],
    teams: [],
    isAdmin: false
  };
}