import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Allow visiting the auth page even if a user exists in localStorage.
  // We won't auto-redirect away from this page so the button works as expected.

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      toast.error("Error", {
        description: "Please fill in all fields.",
      });
      return;
    }

    if (!isLogin && password !== confirmPassword) {
      toast.error("Error", {
        description: "Passwords do not match.",
      });
      return;
    }

    if (!isLogin && password.length < 6) {
      toast.error("Error", {
        description: "Password must be at least 6 characters long.",
      });
      return;
    }

    setIsLoading(true);

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    try {
      if (isLogin) {
        // Check if user exists in localStorage
        const users = JSON.parse(localStorage.getItem("users") || "[]");
        const user = users.find((u) => u.email === email && u.password === password);

        if (!user) {
          throw new Error("Invalid email or password.");
        }

        // Store logged in user
        localStorage.setItem("user", JSON.stringify({ email: user.email }));
        localStorage.setItem("isAuthenticated", "true");

        toast.success("Login Successful", {
          description: "Welcome back!",
        });

        navigate("/dashboard",{replace:true});
      } else {
        // Check if user already exists
        const users = JSON.parse(localStorage.getItem("users") || "[]");
        const existingUser = users.find((u) => u.email === email);

        if (existingUser) {
          throw new Error("User with this email already exists.");
        }

        // Create new user
        const newUser = { email, password };
        users.push(newUser);
        localStorage.setItem("users", JSON.stringify(users));

        // Auto-login after signup
        localStorage.setItem("user", JSON.stringify({ email }));
        localStorage.setItem("isAuthenticated", "true");

        toast.success("Account Created", {
          description: "Your account has been created successfully.",
        });

        navigate("/dashboard",{replace:true});
      }

      setEmail("");
      setPassword("");
      setConfirmPassword("");
    } catch (error) {
      toast.error("Authentication Error", {
        description:
          error.message || "An error occurred during authentication.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
  window.location.href = "http://localhost:8000/login";
};


  const toggleMode = () => {
    setIsLogin(!isLogin);
    setEmail("");
    setPassword("");
    setConfirmPassword("");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[hsl(var(--auth-gradient-start))] to-[hsl(var(--auth-gradient-end))] p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary mb-4">
            <div className="w-8 h-8 border-4 border-primary-foreground rounded-lg" />
          </div>
          <h1 className="text-3xl font-bold text-primary-foreground mb-2">
            {isLogin ? "Welcome Back" : "Create Account"}
          </h1>
          <p className="text-muted-foreground">
            {isLogin
              ? "Enter your credentials to access your account"
              : "Sign up to get started with your account"}
          </p>
        </div>

        <Card className="p-8 backdrop-blur-xl bg-card/50 border-border shadow-[var(--shadow-elegant)]">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-card-foreground">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-background border-border focus:border-primary transition-colors"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-card-foreground">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-background border-border focus:border-primary transition-colors"
                required
              />
            </div>

            {!isLogin && (
              <div className="space-y-2">
                <Label
                  htmlFor="confirmPassword"
                  className="text-card-foreground"
                >
                  Confirm Password
                </Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="bg-background border-border focus:border-primary transition-colors"
                  required
                />
              </div>
            )}

            {isLogin && (
              <div className="flex items-center justify-end">
                <button
                  type="button"
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  Forgot password?
                </button>
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-primary hover:bg-accent transition-all duration-300 shadow-md hover:shadow-lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <span className="animate-spin mr-2">⟳</span>
                  {isLogin ? "Signing in..." : "Creating account..."}
                </span>
              ) : (
                <span>{isLogin ? "Sign In" : "Create Account"}</span>
              )}
            </Button>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>

            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={handleGoogleSignIn}
              disabled={isLoading}
            >
              <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Sign in with Google
            </Button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={toggleMode}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {isLogin ? (
                <>
                  Don't have an account?{" "}
                  <span className="font-semibold text-foreground">Sign up</span>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <span className="font-semibold text-foreground">Sign in</span>
                </>
              )}
            </button>
          </div>
        </Card>

        <p className="text-center text-xs text-muted-foreground mt-8">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
};

export default Auth;
