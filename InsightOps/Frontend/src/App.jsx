import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import NavBar from './components/NavBar';
import HomePage from './components/HomePage';
import GitOrgView from './components/GitOrgView';

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
        path: '/GitOrgView',
        element: <GitOrgView/>
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