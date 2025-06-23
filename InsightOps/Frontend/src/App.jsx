// import { useState, useEffect } from 'react';
// import { BriefcaseIcon, FolderIcon, UsersIcon } from '@heroicons/react/24/solid';
// import { v4 as uuidv4 } from 'uuid';
// import axios from 'axios';
import NavBar from './components/NavBar';
import HomePage from './components/HomePage';
// import OverviewPage from './components/OverviewPage';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import CardList from './components/CardList'
import OrgView from './components/OrgView';

const Layout = () => {
  return (
    <>
      <NavBar />
      <div className="content">
        <Outlet />
      </div>
    </>
  );
};

const router = createBrowserRouter([
  {
    path:'/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <HomePage/>,
      },
      {
        path: '/cardlist',
        element: <CardList/>
      },
      {
        path: '/OrgView',
        element: <OrgView/>
      },

    ]
  }
])


function App() {
  return(
    
    <RouterProvider router={router} />

  )
}

export default App;