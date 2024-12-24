// Task model shape:
// {
//   task_no: number,
//   description: string,
//   timestamp: string,
//   priority: number,
//   hours: number
// }

export const PRIORITY = {
	HIGH: 4, // Green
	MEDIUM: 2, // Yellow
	LOW: 1 // Red
};

export function createTask(task_no, description, timestamp, priority, hours) {
	return {
		task_no,
		description,
		timestamp,
		priority,
		hours
	};
}

export function validateTask(task) {
	return (
		typeof task.task_no === 'number' &&
		typeof task.description === 'string' &&
		typeof task.timestamp === 'string' &&
		typeof task.priority === 'number' &&
		typeof task.hours === 'number' &&
		task.priority >= 1 &&
		task.priority <= 5 &&
		task.hours > 0
	);
}