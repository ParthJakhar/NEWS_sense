
import React from "react";
import CardNav from "../components/CardNav.jsx";
import logo from "../assets/Gemini_Generated_Image_yhkc56yhkc56yhkc (1).png";
import NewsList from "../NewsList.jsx";
import "../App.css";
export default function Dashboard() {
  const items = [
    {
      label: "News",
      bgColor: "#000000ff",
      textColor: "#ffffffff",
      links: [
        { label: "Top Stories", ariaLabel: "#" },
        { label: "World", ariaLabel: "#" },
        { label: "Tech", ariaLabel: "#" },
      ],
    },
    {
      label: "Reddit",
      bgColor: "#08121fff",
      textColor: "#ffffffff",
      links: [
        {
          label: "Trending Threads",
          ariaLabel: "https://reddit.com",
        },
      ],
    },
    {
      label: "About",
      bgColor: "#170a24ff",
      textColor: "#ffffffff",
      links: [
        { label: "Team", ariaLabel: "#" },
        { label: "Contact", ariaLabel: "#" },
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100 relative">
      {/* Navigation Bar */}
      <CardNav
        logo={logo}
        logoAlt="NewsSense"
        items={items}
        buttonBgColor="#000000ff"
        buttonTextColor="#fff"
        menuColor="#000000ff"
      />

      {/* News Section */}
      <div className="mt-10">
        <NewsList />
      </div>
    </div>
  );
}
