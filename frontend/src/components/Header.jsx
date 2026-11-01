
import { Bell, UserCircle } from 'lucide-react';

const Header = () => {
  return (
    <header className="header">
      <h3>Notification Management</h3>

      <div className="header-actions">
        <Bell size={21} />
        <UserCircle size={25} />
      </div>
    </header>
  );
};

export default Header;
