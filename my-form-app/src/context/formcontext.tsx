
import { createContext, useState, ReactNode } from "react";

interface FormData {
  fullName: string;
  email: string;
  phone: string;
  age: number;
  language: string;
}

interface FormContextType {
  formData: FormData;
  setFormData: (data: FormData) => void;
}

export const FormContext = createContext<FormContextType | null>(null);

export const FormProvider = ({ children }: { children: ReactNode }) => {
  const [formData, setFormData] = useState<FormData>({
    fullName: "",
    email: "",
    phone: "",
    age: 0,
    language: "",
  });

  return (
    <FormContext.Provider value={{ formData, setFormData }}>
      {children}
    </FormContext.Provider>
  );
};
