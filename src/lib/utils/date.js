export function getDaysInMonth(date) {
	const year = date.getFullYear();
	const month = date.getMonth();
	const firstDay = new Date(year, month, 1).getDay();
	const totalDays = new Date(year, month + 1, 0).getDate();
	
	let days = Array(firstDay).fill(null);
	for (let i = 1; i <= totalDays; i++) {
		days.push(i);
	}
	return days;
}

export function formatDate(date) {
	return date.toISOString().split('T')[0];
}