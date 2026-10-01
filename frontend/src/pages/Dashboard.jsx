export default function Dashboard() {
  return (
    <div style={styles.page}>
      <h1>PDF Analysis Platform</h1>
      <p>Welcome to your dashboard</p>

      <div style={styles.card}>
        <h3>PDF Analyzer</h3>
        <p>Upload PDFs, highlight text, extract tables, and visualize data.</p>

        {/* 🔗 Link to HTML split view */}
        <a href="/app/" style={styles.btn}>
          Open Analyzer
        </a>
      </div>
    </div>
  );
}

const styles = {
  page: {
    padding: "40px",
    fontFamily: "Segoe UI",
  },
  card: {
    marginTop: "30px",
    padding: "20px",
    border: "1px solid #38bdf8",
    borderRadius: "12px",
    maxWidth: "400px",
  },
  btn: {
    display: "inline-block",
    marginTop: "10px",
    padding: "10px 20px",
    background: "#38bdf8",
    color: "#020617",
    borderRadius: "20px",
    textDecoration: "none",
    fontWeight: "600",
  },
};
