import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Servers from './pages/Servers';
import Groups from './pages/Groups';
import Tags from './pages/Tags';
import Reports from './pages/Reports';
import Schedules from './pages/Schedules';
import Login from './pages/Login';
import TagMonitor from './pages/TagMonitor';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="*"
        element={
          <ProtectedRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/servers" element={<Servers />} />
                <Route path="/groups" element={<Groups />} />
                <Route path="/tags" element={<Tags />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/schedules" element={<Schedules />} />
                <Route path="/monitor" element={<TagMonitor />} />
              </Routes>
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
