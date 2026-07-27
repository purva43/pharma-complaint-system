import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { loginStart, loginSuccess, loginFailure } from '../../store/slices/authSlice';
import { authAPI } from '../../api/auth';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';
import Spinner from '../../components/common/Spinner';
import toast from 'react-hot-toast';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    dispatch(loginStart());

    try {
      const response = await authAPI.login(formData.email, formData.password);
      dispatch(loginSuccess({ token: response.access_token, user: null }));
      toast.success('Login successful');
      navigate('/dashboard');
    } catch (error) {
      dispatch(loginFailure(error.response?.data?.detail || 'Login failed'));
      toast.error('Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <Card className="w-full max-w-md">
        <div className="px-8 py-8">
          <h1 className="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">
            Pharma Complaint Management System
          </h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
            <Input
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? <Spinner size="sm" /> : 'Login'}
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
};

export default Login;
