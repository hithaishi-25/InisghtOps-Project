const Sidebar = ({ isOpen, toggleSidebar }) => {
  return (
    <div className={`fixed md:relative z-50 ${isOpen ? "w-64" : "w-16"} bg-blue-900 text-white h-screen p-4 transition-width duration-300`}>
      <button className="md:hidden mb-4 text-lg" onClick={toggleSidebar}>☰</button>
      <h2 className="text-xl font-bold mb-4">InsightOps</h2>
      <ul className="space-y-2">
        {[
          "Org Overview", "Project Details", "Query Work Items", "User Groups",
          "Activities", "Kanban", "Commits", "Pull Requests", "Approver",
        ].map((item, index) => (
          <li key={index} className="hover:bg-blue-700 p-2 rounded">{item}</li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;