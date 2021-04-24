import axios from 'axios';

const getPastes = async (offset: number, limit: number, user: string | null = null) => {
  const params = (user === null) ? { offset, limit } : { offset, limit, user };
  const result = await axios.get('/api/pastes', { params });
  return result;
};

export default getPastes;
