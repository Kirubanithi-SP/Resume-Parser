// frontend/src/services/authService.js
import apiClient from './api';

const login = async (username, password) => {
  try {
    const response = await apiClient.post('/auth/login', { username, password });
    // Assuming the backend returns { access_token: "..." }
    if (response.data && response.data.access_token) {
      return response.data.access_token;
    } else {
      throw new Error('Login failed: No access token received');
    }
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    // Throw a more specific error message if available from backend
    throw new Error(error.response?.data?.message || 'Login failed. Please check your credentials.');
  }
};

// Optional: Add registration function if needed
const register = async (username, password) => {
     try {
       const response = await apiClient.post('/auth/register', { username, password });
       return response.data; // e.g., { message: "User registered successfully" }
     } catch (error) {
       console.error('Registration error:', error.response?.data || error.message);
       throw new Error(error.response?.data?.message || 'Registration failed.');
     }
};

// Optional: Function to verify token / get user info
const verifyToken = async () => {
    try {
        // Assumes the interceptor adds the token
        const response = await apiClient.get('/auth/me');
        return response.data; // e.g., { username: "..." }
    } catch (error) {
        console.error('Token verification error:', error.response?.data || error.message);
        // Don't throw here necessarily, just indicate failure
        return null;
    }
}


export const authService = {
  login,
  register, // Uncomment if you implement registration UI
  verifyToken,
};