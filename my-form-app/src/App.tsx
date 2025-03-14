
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Form from "./component/form";
import Summary from "./pages/summary";
import { FormProvider } from "./context/formcontext";

const App = () => {
  return (
    <FormProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Form />} />
          <Route path="/summary" element={<Summary />} />
        </Routes>
      </Router>
    </FormProvider>
  );
};

export default App;
