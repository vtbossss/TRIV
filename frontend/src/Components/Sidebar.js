import React from 'react'
import { Link } from 'react-router-dom'

const Sidebar = () => {
  return (
    <div className="bg-gray-800 h-screen w-64 text-white absolute top-13 left-0 shadow-lg">
      {/* <div className="p-4 text-1xl font-bold bg-green-600">
        LOGO
      </div> */}
      <nav className="mt-5 space-y-2">
        
        {/* Basic Links */}
        <Link to="/" className="block py-2.5 px-4 rounded hover:bg-green-600">Home</Link>
        <Link to="/dataInfo" className="block py-2.5 px-4 rounded hover:bg-green-600">Agro Data</Link>
        <Link to="/weather" className="block py-2.5 px-4 rounded hover:bg-green-600">Weather</Link>
        <Link to="/ndvi" className="block py-2.5 px-4 rounded hover:bg-green-600">NDVI</Link>

        {/* Additional Links */}
        <Link to="/data-management" className="block py-2.5 px-4 rounded hover:bg-green-600">Data Management</Link>
        <Link to="/analytics-tools" className="block py-2.5 px-4 rounded hover:bg-green-600">Analytics Tools</Link>
        <Link to="/settings" className="block py-2.5 px-4 rounded hover:bg-green-600">Settings</Link>
        <Link to="/support" className="block py-2.5 px-4 rounded hover:bg-green-600">Support</Link>
        <Link to="/about" className="block py-2.5 px-4 rounded hover:bg-green-600">About</Link>
        
      </nav>
    </div>
  )
}

export default Sidebar