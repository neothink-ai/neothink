// Team model shape:
// {
//   id: string,
//   name: string,
//   description: string,
//   members: string[], // Array of user IDs
//   createdBy: string, // User ID of team creator
//   createdAt: timestamp
// }

export function createTeam(name, description, createdBy) {
  return {
    name,
    description,
    members: [createdBy],
    createdBy,
    createdAt: new Date().toISOString()
  };
}