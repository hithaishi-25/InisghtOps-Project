import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import NavBar from './components/NavBar';
import HomePage from './components/HomePage';
import GitOrgView from './components/GitOrgView';
import ViewReport from './components/ViewReports';
const Layout = () => {
  return (
    <>
    <NavBar/>
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
      { 
        // 1. Change the path to accept a dynamic segment for the org name
        path: '/view-report', 
        element: <ViewReport />
      },
    ]
  }
])


function App() {
  return(
    <div>
    <RouterProvider router={router} />
    </div>

  )
}

export default App;