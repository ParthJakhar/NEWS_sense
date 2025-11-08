import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold text-foreground">Welcome to Your App</h1>
        <p className="text-xl text-muted-foreground">Ready to get started?</p>
        <Button
          onClick={() => navigate("/auth",{replace:true})}
          size="lg"
          className="bg-primary hover:bg-accent transition-all duration-300"
        >
          Go
        </Button>
      </div>
    </div>
  );
};

export default Index;
