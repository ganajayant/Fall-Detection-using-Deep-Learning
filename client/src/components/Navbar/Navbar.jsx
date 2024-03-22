import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";


const Header = () => {
  return (
    <>
      <div className="header">
        <Link to={'/'}>
          <div className="logo">
            <span>F</span>all <span>D</span>etection <span>S</span>ystem
          </div>
        </Link>
        <ul className="navbar">
          <li className="nav-item">
            <a href="/">home</a>
          </li>
        </ul>
      </div>
    </>
  );
};

export default Header;
