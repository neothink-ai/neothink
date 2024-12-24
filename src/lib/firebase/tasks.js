import { 
  collection,
  addDoc,
  query,
  where,
  getDocs,
  Timestamp
} from 'firebase/firestore';
import { db } from './firebase';

export async function addTask(userId, task) {
  try {
    const taskData = {
      ...task,
      userId,
      timestamp: Timestamp.fromDate(new Date(task.timestamp)),
      created_at: Timestamp.now()
    };
    
    const docRef = await addDoc(collection(db, 'tasks'), taskData);
    return docRef.id;
  } catch (error) {
    throw new Error('Error adding task: ' + error.message);
  }
}

export async function getTasksForDate(userId, date) {
  try {
    const startOfDay = new Date(date);
    startOfDay.setHours(0, 0, 0, 0);
    
    const endOfDay = new Date(date);
    endOfDay.setHours(23, 59, 59, 999);
    
    const tasksQuery = query(
      collection(db, 'tasks'),
      where('userId', '==', userId),
      where('timestamp', '>=', Timestamp.fromDate(startOfDay)),
      where('timestamp', '<=', Timestamp.fromDate(endOfDay))
    );
    
    const querySnapshot = await getDocs(tasksQuery);
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
      timestamp: doc.data().timestamp.toDate()
    }));
  } catch (error) {
    throw new Error('Error fetching tasks: ' + error.message);
  }
}