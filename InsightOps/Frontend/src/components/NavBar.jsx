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
          {navItems.map((item) => (
            <li 
              key={item.name}
              className={activeLink === item.name.toLowerCase() ? 'active' : ''}
              onClick={() => setActiveLink(item.name.toLowerCase())}
            >
              <Link to={item.path}>
                <span className="icon">{item.icon}</span>
                <span className="text">{item.name}</span>
              </Link>
            </li>
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
