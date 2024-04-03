import {BrowserRouter, Route, Routes} from 'react-router-dom'
import Dashboard from './pages/Dashboard';
import Parameter from './pages/Parameter';
import Details from './pages/Details';
import Template from "./pages/template"


const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path={"/"} element ={<Dashboard/>}/>
        <Route path={"/parameter"} element ={<Parameter/>}/>
        <Route path={"/details"} element ={<Details/>}/>
        <Route path={"/template"} element ={<Template/>}/>
      </Routes>
    </BrowserRouter>

  );
}

export default App;
