import { useContext } from "react";
import { FormContext } from "../context/formcontext";
import { useNavigate } from "react-router-dom";

const Summary = () => {
  const formContext = useContext(FormContext);
  if (!formContext) return null;
  const { formData } = formContext;

  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold text-center mb-6">Submitted Details</h2>
        <div className="space-y-4">
          <p><strong>Full Name:</strong> {formData.fullName}</p>
          <p><strong>Email:</strong> {formData.email}</p>
          <p><strong>Phone:</strong> {formData.phone}</p>
          <p><strong>Age:</strong> {formData.age}</p>
          <p><strong>Favorite Language:</strong> {formData.language}</p>
        </div>
        <button onClick={() => navigate("/")} className="mt-6 w-full bg-gray-500 text-white py-2 rounded hover:bg-gray-600">
          Go Back
        </button>
      </div>
    </div>
  );
};

export default Summary;
