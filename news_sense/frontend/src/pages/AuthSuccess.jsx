// src/pages/AuthSuccess.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

export default function AuthSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const name = params.get("name");
    const email = params.get("email");
    const picture = params.get("picture");

    if (email) {
      const user = { name, email, picture };
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("isAuthenticated", "true");

      toast.success("Google Sign-In Successful", {
        description: `Welcome, ${name}!`,
      });

      navigate("/");
    } else {
      toast.error("Authentication Failed");
      navigate("/auth");
    }
  }, [navigate]);

  return (
    <div className="flex justify-center items-center h-screen text-lg">
      Redirecting...
    </div>
  );
}
