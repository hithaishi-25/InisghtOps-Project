import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import NavBar from './components/NavBar';
import HomePage from './components/HomePage';
import GitOrgView from './components/GitOrgView';
import Projects from './components/Projects';
import Repositories from './components/Repositories';
import Users from './components/Users';
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
        element: <GitOrgView/>,
      },
      {
        path: '/projects',
        element: <Projects/>,
      },
      {
        path: '/repositories',
        element: <Repositories/>,
      },
      {
        path: '/users',
        element: <Users/>,
      },
      { 
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