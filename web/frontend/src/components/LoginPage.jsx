import { useState } from 'react';
import './LoginPage.css';

const API_URL = 'http://127.0.0.1:8000';

/**
 * LoginPage Component
 * 
 * Provides user authentication UI.
 */
function LoginPage({ isOpen, onClose, onLogin, language = 'zh-tw' }) {
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const translations = {
    'zh-tw': {
      login: '登入',
      register: '註冊',
      username: '使用者名稱',
      email: '電子郵件',
      password: '密碼',
      confirmPassword: '確認密碼',
      loginButton: '登入',
      registerButton: '註冊',
      switchToRegister: '還沒有帳號？註冊',
      switchToLogin: '已有帳號？登入',
      loggingIn: '登入中...',
      registering: '註冊中...',
      loginSuccess: '登入成功！',
      registerSuccess: '註冊成功！請登入',
      passwordMismatch: '密碼不一致',
      fillAllFields: '請填寫所有欄位',
      welcomeBack: '歡迎回來',
      createAccount: '建立帳號'
    },
    'en': {
      login: 'Login',
      register: 'Register',
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      loginButton: 'Login',
      registerButton: 'Register',
      switchToRegister: "Don't have an account? Register",
      switchToLogin: 'Already have an account? Login',
      loggingIn: 'Logging in...',
      registering: 'Registering...',
      loginSuccess: 'Login successful!',
      registerSuccess: 'Registration successful! Please login',
      passwordMismatch: 'Passwords do not match',
      fillAllFields: 'Please fill all fields',
      welcomeBack: 'Welcome Back',
      createAccount: 'Create Account'
    },
    'ja': {
      login: 'ログイン',
      register: '登録',
      username: 'ユーザー名',
      email: 'メールアドレス',
      password: 'パスワード',
      confirmPassword: 'パスワード確認',
      loginButton: 'ログイン',
      registerButton: '登録',
      switchToRegister: 'アカウントをお持ちでない方は登録',
      switchToLogin: 'アカウントをお持ちの方はログイン',
      loggingIn: 'ログイン中...',
      registering: '登録中...',
      loginSuccess: 'ログイン成功！',
      registerSuccess: '登録成功！ログインしてください',
      passwordMismatch: 'パスワードが一致しません',
      fillAllFields: 'すべての項目を入力してください',
      welcomeBack: 'おかえりなさい',
      createAccount: 'アカウント作成'
    },
    'zh-cn': {
      login: '登录',
      register: '注册',
      username: '用户名',
      email: '电子邮件',
      password: '密码',
      confirmPassword: '确认密码',
      loginButton: '登录',
      registerButton: '注册',
      switchToRegister: '没有账号？注册',
      switchToLogin: '已有账号？登录',
      loggingIn: '登录中...',
      registering: '注册中...',
      loginSuccess: '登录成功！',
      registerSuccess: '注册成功！请登录',
      passwordMismatch: '密码不一致',
      fillAllFields: '请填写所有字段',
      welcomeBack: '欢迎回来',
      createAccount: '创建账号'
    }
  };

  const tr = translations[language] || translations['zh-tw'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
    setSuccess('');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!formData.username || !formData.password) {
      setError(tr.fillAllFields);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username_or_email: formData.username,
          password: formData.password
        })
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Login failed');
      }
      
      const data = await response.json();
      setSuccess(tr.loginSuccess);
      
      if (onLogin) {
        onLogin(data);
      }
      
      setTimeout(() => {
        onClose();
      }, 1000);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (!formData.username || !formData.email || !formData.password) {
      setError(tr.fillAllFields);
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError(tr.passwordMismatch);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        })
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Registration failed');
      }
      
      setSuccess(tr.registerSuccess);
      setMode('login');
      setFormData(prev => ({ ...prev, password: '', confirmPassword: '' }));
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="login-overlay" onClick={onClose}>
      <div className="login-panel" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>✕</button>
        
        <div className="login-header">
          <h2>{mode === 'login' ? tr.welcomeBack : tr.createAccount}</h2>
        </div>
        
        <form onSubmit={mode === 'login' ? handleLogin : handleRegister}>
          <div className="form-group">
            <label>{tr.username}</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder={tr.username}
              disabled={loading}
            />
          </div>
          
          {mode === 'register' && (
            <div className="form-group">
              <label>{tr.email}</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder={tr.email}
                disabled={loading}
              />
            </div>
          )}
          
          <div className="form-group">
            <label>{tr.password}</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder={tr.password}
              disabled={loading}
            />
          </div>
          
          {mode === 'register' && (
            <div className="form-group">
              <label>{tr.confirmPassword}</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder={tr.confirmPassword}
                disabled={loading}
              />
            </div>
          )}
          
          {error && <p className="error-message">{error}</p>}
          {success && <p className="success-message">{success}</p>}
          
          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading 
              ? (mode === 'login' ? tr.loggingIn : tr.registering)
              : (mode === 'login' ? tr.loginButton : tr.registerButton)
            }
          </button>
        </form>
        
        <button 
          className="switch-mode-button"
          onClick={() => {
            setMode(mode === 'login' ? 'register' : 'login');
            setError('');
            setSuccess('');
          }}
        >
          {mode === 'login' ? tr.switchToRegister : tr.switchToLogin}
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
