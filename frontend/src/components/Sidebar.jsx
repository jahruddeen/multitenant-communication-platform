
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Building2,
  Users,
  MessageSquare,
  Phone,
  FileText,
  LogOut
} from 'lucide-react';

const Sidebar = () => {
  const navigate = useNavigate();

  const menuItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Companies', path: '/companies', icon: Building2 },
    { name: 'Contacts', path: '/contacts', icon: Users },
    { name: 'SMS', path: '/sms', icon: MessageSquare },
    { name: 'Voice Calls', path: '/calls', icon: Phone },
    { name: 'Reports', path: '/reports', icon: FileText }
  ];

  const handleLogout = () => {
    sessionStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <h2 className="sidebar-logo">NotifyHub</h2>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <Icon size={19} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      <button className="logout-button" onClick={handleLogout}>
        <LogOut size={19} />
        <span>Logout</span>
      </button>
    </aside>
  );
};

export default Sidebar;
