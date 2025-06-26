import { useState } from "react";
import { Link } from 'react-router-dom';

import { FiHome, FiUser, FiMail,FiClock, FiMenu, FiX } from "react-icons/fi";
import '../NavBar.css';

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeLink, setActiveLink] = useState('home');

  const toggleMenu = () => setIsOpen(!isOpen);

  const navItems =[
    { name: 'Home', path: '/', icon: <FiHome /> },
    { name: 'About', path: '/about', icon: <FiUser /> },
    { name: 'Contact', path: '/contact', icon: <FiMail /> },
    { name: 'Timer', path: '/timer', icon: <FiClock /> }
  ]
  return (
    <nav className={ `navbar ${isOpen ? 'open' : ''}` }>

      <div className="toggle-btn" onClick={toggleMenu}>
        {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </div>

      <div className="navbar-conetent">
        <div className="logo"></div>
        <ul className="nav-links">
        {[
          "Org Overview", "Project Details", "Query Work Items", "User Groups",
          "Activities", "Kanban", "Commits", "Pull Requests", "Approver",
        ].map((item, index) => (
          <li key={index} className="hover:bg-blue-700 p-2 rounded">{item}</li>
        ))}
        </ul>

        <div className="user-profile">
          <div className="avatar">U</div>
          {isOpen && <div className="username">Username</div>}
        </div>
      </div>

    </nav>
  )
}

export default NavBar;
