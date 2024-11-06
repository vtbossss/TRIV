import React from 'react'

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
          <a href="/" className="hover:text-gray-200">Home</a>
          <a href="/data-sources" className="hover:text-gray-200">Data Sources</a>
          <a href="/about" className="hover:text-gray-200">About</a>
        </div>
        
        {/* Optional: Theme Toggle */}
        <button className="bg-white text-green-600 px-2 py-1 rounded hover:bg-gray-200">
          Toggle Theme
        </button>
        
      </div>
    </nav>
    </div>
  )
}

export default Navbar