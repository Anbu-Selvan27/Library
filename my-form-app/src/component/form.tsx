import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { FormContext } from "../context/formcontext";

const schema = yup.object().shape({
  fullName: yup.string().required("Full Name is required"),
  email: yup.string().email("Invalid email").required("Email is required"),
  phone: yup.string().matches(/^\d+$/, "Phone number must be digits").required("Phone is required"),
  age: yup.number().positive().integer().required("Age is required"),
  language: yup.string().required("Please select a programming language"),
});

interface FormValues {
  fullName: string;
  email: string;
  phone: string;
  age: number;
  language: string;
}

const Form = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: yupResolver(schema),
  });

  const formContext = useContext(FormContext);
  if (!formContext) return null;
  const { setFormData } = formContext;

  const navigate = useNavigate();

  const onSubmit = (data: FormValues) => {
    setFormData(data);
    navigate("/summary");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold text-center mb-6">Personal Details</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-gray-700 font-medium">Full Name</label>
            <input {...register("fullName")} className="w-full p-2 border rounded" />
            <p className="text-red-500 text-sm">{errors.fullName?.message}</p>
          </div>

          <div>
            <label className="block text-gray-700 font-medium">Email</label>
            <input type="email" {...register("email")} className="w-full p-2 border rounded" />
            <p className="text-red-500 text-sm">{errors.email?.message}</p>
          </div>

          <div>
            <label className="block text-gray-700 font-medium">Phone Number</label>
            <input type="text" {...register("phone")} className="w-full p-2 border rounded" />
            <p className="text-red-500 text-sm">{errors.phone?.message}</p>
          </div>

          <div>
            <label className="block text-gray-700 font-medium">Age</label>
            <input type="number" {...register("age")} className="w-full p-2 border rounded" />
            <p className="text-red-500 text-sm">{errors.age?.message}</p>
          </div>

          <div>
            <label className="block text-gray-700 font-medium">Favorite Programming Language</label>
            <select {...register("language")} className="w-full p-2 border rounded">
              <option value="">Select a language</option>
              <option value="Python">Python</option>
              <option value="JavaScript">JavaScript</option>
              <option value="Java">Java</option>
              <option value="C++">C++</option>
            </select>
            <p className="text-red-500 text-sm">{errors.language?.message}</p>''
          </div>

          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default Form;
