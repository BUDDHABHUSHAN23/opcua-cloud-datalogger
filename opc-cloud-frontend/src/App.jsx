import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Servers from './pages/Servers';
import Groups from './pages/Groups';
import Tags from './pages/Tags';
import Reports from './pages/Reports';
import Schedules from './pages/Schedules';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/servers" element={<Servers />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/tags" element={<Tags />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/schedules" element={<Schedules />} />
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </BrowserRouter>
  );
}
