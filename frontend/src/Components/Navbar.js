import React from 'react'
// import { Routes, Route } from 'react-router-dom'
// import MainHeader from '../Pages/MainHeader'
// import Home from '../Pages/Home'
// import DataInfo from '../Pages/DataInfo'
// import About from '../Pages/About'
import { NavLink } from 'react-router-dom'

const Navbar = () => {
  return (
    <div>
        <nav className="bg-green-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        L.O.G.O.
        {/* Logo */}
        <div className="text-2xl font-bold">
          AgriData3D
        </div>
        
        {/* Navigation Links */}
        <div className="flex space-x-4">
        
          <NavLink to="/" className="hover:text-gray-200">Home</NavLink>
            <NavLink to="/dataInfo" className="hover:text-gray-200">Data Sources</NavLink>
            <NavLink to="/about" className="hover:text-gray-200">About</NavLink>

        </div>
        
        {/* Optional: Theme Toggle */}
        <button className="bg-white text-green-600 px-2 py-1 rounded hover:bg-gray-200">
          Toggle Theme
        </button>
        
      </div>

      {/* <Routes>
        <Route path="/" element={<MainHeader />} />
        <Route index element={<Home />} />
        <Route path="/dataInfo" element={<DataInfo />} />
        <Route path="/about" element={<About />} />
     </Routes> */}

    </nav>
    </div>
  )
}

export default Navbar