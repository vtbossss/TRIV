import React from 'react'
// import { Routes, Route } from 'react-router-dom'
// import MainHeader from '../Pages/MainHeader'
// import Home from '../Pages/Home'
// import DataInfo from '../Pages/DataInfo'
// import About from '../Pages/About'
import { NavLink } from 'react-router-dom'
import { GiHamburgerMenu } from "react-icons/gi";


const Navbar = (props) => {
  const { toggleSidebar } = props;
  return (
   
        <nav className="bg-green-600 text-white ">
      <div className=" px-4 py-3 flex items-center justify-between ">
      <button className='text-2xl font-bold' onClick={toggleSidebar}><GiHamburgerMenu /></button>
       <div> L.O.G.O.</div>
        {/* Logo */}
        <div className="text-2xl font-bold">
          AgriData3D
        </div>
        
        {/* Navigation Links */}
        <div className="flex space-x-4">
        
          <NavLink to="/" className="hover:text-gray-200">Home</NavLink>
            <NavLink to="/dataInfo" className="hover:text-gray-200">Agro Data</NavLink>
        <NavLink to="/weather" className="hover:text-gray-200">Weather</NavLink>
        <NavLink to="/ndvi" className="hover:text-gray-200">NDVI</NavLink>

        </div>
        
        {/* Optional: Theme Toggle */}
        
        <div>
        <button className="bg-white text-green-600 px-2 py-1 rounded hover:bg-gray-200 mx-5">
          Log In
        </button>

        <button className="bg-white text-green-600 px-2 py-1 rounded hover:bg-gray-200">
          Sign Up
        </button>
        </div>
        
      </div>

      {/* <Routes>
        <Route path="/" element={<MainHeader />} />
        <Route index element={<Home />} />
        <Route path="/dataInfo" element={<DataInfo />} />
        <Route path="/about" element={<About />} />
     </Routes> */}

    </nav>
    
  )
}

export default Navbar