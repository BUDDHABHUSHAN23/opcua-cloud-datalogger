import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex gap-6">
      <Link to="/" className="hover:underline">Dashboard</Link>
      <Link to="/servers" className="hover:underline">Servers</Link>
      <Link to="/groups" className="hover:underline">Groups</Link>
      <Link to="/tags" className="hover:underline">Tags</Link>
      <Link to="/reports" className="hover:underline">Reports</Link>
      <Link to="/schedules" className="hover:underline">Schedules</Link>
      <Link to="/monitor" className="hover:underline">Monitor</Link>
      <Link to="/tag-tree" className="hover:underline">Tag Tree</Link>
    </nav>
  );
}
