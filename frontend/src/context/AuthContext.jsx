import { createContext, useContext, useState, useEffect, useCallback } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  // Load user profile on mount if token exists
  useEffect(() => {
    if (token) {
      loadProfile();
    } else {
      setLoading(false);
    }
  }, []);

  const loadProfile = async () => {
    try {
      const response = await api.get("/api/v1/auth/me");
      setUser(response.data.data);
    } catch {
      // Token invalid or expired
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (email, password) => {
    const response = await api.post("/api/v1/auth/login", { email, password });
    const { user: userData, token: authToken } = response.data.data;
    setUser(userData);
    setToken(authToken);
    localStorage.setItem("token", authToken);
    return userData;
  }, []);

  const register = useCallback(async (name, email, password, location) => {
    const response = await api.post("/api/v1/auth/register", {
      name,
      email,
      password,
      location,
    });
    const { user: userData, token: authToken } = response.data.data;
    setUser(userData);
    setToken(authToken);
    localStorage.setItem("token", authToken);
    return userData;
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  }, []);

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default AuthContext;
