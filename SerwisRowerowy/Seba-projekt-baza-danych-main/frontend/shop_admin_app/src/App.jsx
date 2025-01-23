import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Clients from './components/Clients';
import Bikes from './components/Bikes';
import Orders from './components/Orders';
import Services from './components/Services';
import Employees from './components/Employees';
import { useState, useEffect, useRef } from 'react';

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeMenu, setActiveMenu] = useState(null);
  const menuRef = useRef(null);

  const closeMenu = () => {
    setMenuOpen(false);
    setActiveMenu(null);
  };

  const handleClickOutside = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      closeMenu();
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleMenuClick = (menu) => {
    setActiveMenu(activeMenu === menu ? null : menu);
  };

  const adjustMenuPosition = (menu) => {
    if (menu) {
      const rect = menu.getBoundingClientRect();
      if (rect.right > window.innerWidth) {
        menu.style.left = `-${rect.right - window.innerWidth}px`;
      }
    }
  };

  useEffect(() => {
    if (activeMenu) {
      const menu = document.querySelector(`#${activeMenu}`);
      adjustMenuPosition(menu);
    }
  }, [activeMenu]);

  const exportData = () => {
    fetch('http://localhost:5000/api/export')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data); // Log the response data
        if (data.message && data.data) {
          const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'exported_data.json';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error);
      });
  };

  return (
    <Router>
      <div className="container mx-auto p-4 md:px-10">
        <header className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center py-4 bg-gray-700 text-white shadow-md">
          <div className="flex items-center">
            <Link to="/" className="px-4 py-2 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7m-9 2v8m-4-4h8" />
              </svg>
            </Link>
            <h1 className="text-lg md:text-2xl">System zarządzania sklepem rowerowym</h1>
          </div>
          <div className="relative flex items-center">
            <button
              className="md:hidden text-black-white"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              ☰
            </button>
            <nav
              ref={menuRef}
              className={`fixed top-0 right-0 h-full bg-gray-800 text-white transform ${
                menuOpen ? 'translate-x-0' : 'translate-x-full'
              } transition-transform duration-300 ease-out md:relative md:transform-none md:bg-transparent md:text-white md:shadow-none`}
            >
              <div className="flex justify-end p-4 md:hidden">
                <button onClick={closeMenu} className="text-white text-xl font-bold">×</button>
              </div>
              <ul className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
                <li className="group relative">
                  <span
                    className="block px-2 py-1 md:inline-block"
                    onClick={() => handleMenuClick('orders-menu')}
                  >
                    Zamówienia <span className={`arrow ${activeMenu === 'orders-menu' ? 'rotate-180' : ''}`}>▼</span>
                  </span>
                  <ul
                    id="orders-menu"
                    className={`absolute left-0 mt-2 bg-white text-black rounded-lg shadow-lg ${
                      activeMenu === 'orders-menu' ? 'block' : 'hidden'
                    }`}
                  >
                    <li>
                      <Link to="/clients" className="block px-4 py-2" onClick={closeMenu}>
                        Klienci
                      </Link>
                    </li>
                    <li>
                      <Link to="/bikes" className="block px-4 py-2" onClick={closeMenu}>
                        Rowery
                      </Link>
                    </li>
                    <li>
                      <Link to="/services" className="block px-4 py-2" onClick={closeMenu}>
                        Usługi
                      </Link>
                    </li>
                  </ul>
                </li>
                <li className="group relative">
                  <span
                    className="block px-2 py-1 md:inline-block"
                    onClick={() => handleMenuClick('employees-menu')}
                  >
                    Pracownicy <span className={`arrow ${activeMenu === 'employees-menu' ? 'rotate-180' : ''}`}>▼</span>
                  </span>
                  <ul
                    id="employees-menu"
                    className={`absolute left-0 mt-2 bg-white text-black rounded-lg shadow-lg ${
                      activeMenu === 'employees-menu' ? 'block' : 'hidden'
                    }`}
                  >
                    <li>
                      <Link to="/employees" className="block px-4 py-2" onClick={closeMenu}>
                        Lista pracowników
                      </Link>
                    </li>
                    <li>
                      <Link to="/orders" className="block px-4 py-2" onClick={closeMenu}>
                        Zlecenia
                      </Link>
                    </li>
                  </ul>
                </li>
                <li className="group relative">
                  <span
                    className="block px-2 py-1 md:inline-block"
                    onClick={() => handleMenuClick('options-menu')}
                  >
                    Opcje <span className={`arrow ${activeMenu === 'options-menu' ? 'rotate-180' : ''}`}>▼</span>
                  </span>
                  <ul
                    id="options-menu"
                    className={`absolute left-0 mt-2 bg-white text-black rounded-lg shadow-lg ${
                      activeMenu === 'options-menu' ? 'block' : 'hidden'
                    }`}
                  >
                    <li>
                      <Link to="#" onClick={exportData} className="block px-4 py-2 text-blue-600">
                        Eksportuj bazę do pliku JSON
                      </Link>
                    </li>
                  </ul>
                </li>
              </ul>
            </nav>
          </div>
        </header>
        <div className="pt-20" onClick={closeMenu}>
          <Routes>
            <Route path="/" element={<h1 className="text-3xl font-bold">Witamy w systemie zarządzania sklepem rowerowym</h1>} />
            <Route path="/clients" element={<Clients />} />
            <Route path="/bikes" element={<Bikes />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/services" element={<Services />} />
            <Route path="/employees" element={<Employees />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;