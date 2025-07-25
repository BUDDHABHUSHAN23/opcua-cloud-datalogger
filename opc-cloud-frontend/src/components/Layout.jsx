
import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function Layout({ children }) {
  const { logout } = useContext(AuthContext);
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-700 text-white px-4 py-2 flex justify-between">
        <div className="space-x-4">
          <Link to="/" className="hover:underline">Home</Link>
          <Link to="/dashboard" className="hover:underline">Dashboard</Link>
          <Link to="/servers" className="hover:underline">Servers</Link>
          <Link to="/groups" className="hover:underline">Groups</Link>
          <Link to="/tags" className="hover:underline">Tags</Link>
          <Link to="/reports" className="hover:underline">Reports</Link>
          <Link to="/schedules" className="hover:underline">Schedules</Link>
          <Link to="/monitor" className="hover:underline">Monitor</Link>
          <Link to="/tag-tree" className="hover:underline">Tag Tree</Link>
        </div>
        <button onClick={logout} className="hover:underline">Logout</button>
      </nav>
      <main className="p-4">{children}</main>
    </div>
  );
}
