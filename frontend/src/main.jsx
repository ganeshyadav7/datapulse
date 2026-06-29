import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Database,
  GitBranch,
  Moon,
  Search,
  Shield,
  Sparkles,
  Sun
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const views = [
  { id: "dashboard", label: "Dashboard", icon: Activity },
  { id: "pipelines", label: "Pipelines", icon: GitBranch },
  { id: "airflow", label: "Airflow", icon: BarChart3 },
  { id: "spark", label: "Spark", icon: Sparkles },
  { id: "quality", label: "Data Quality", icon: Shield },
  { id: "metrics", label: "Metrics", icon: Database }
];

function statusClass(status) {
  const normalized = String(status || "").toLowerCase();
  if (normalized === "success") return "status success";
  if (normalized === "failed") return "status failed";
  if (normalized === "running") return "status running";
  return "status neutral";
}

async function fetchJson(path, token) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

function Login({ onLogin }) {
  const [email, setEmail] = useState("admin@datapulse.local");
  const [password, setPassword] = useState("password123");
  const [message, setMessage] = useState("");

  async function submit(event) {
    event.preventDefault();
    setMessage("Signing in...");
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      if (!response.ok) throw new Error("Login failed");
      const data = await response.json();
      onLogin(data.access_token);
      setMessage("Signed in");
    } catch {
      setMessage("Login requires a registered user when AUTH_ENABLED=true.");
    }
  }

  return (
    <form className="login" onSubmit={submit}>
      <h2>DataPulse</h2>
      <input value={email} onChange={(event) => setEmail(event.target.value)} />
      <input
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <button type="submit">Login</button>
      <p>{message}</p>
    </form>
  );
}

function Card({ title, value, tone }) {
  return (
    <section className={`metric-card ${tone || ""}`}>
      <span>{title}</span>
      <strong>{value}</strong>
    </section>
  );
}

function DataTable({ rows, columns }) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const pageSize = 10;
  const filtered = useMemo(() => {
    const lower = query.toLowerCase();
    return rows.filter((row) => JSON.stringify(row).toLowerCase().includes(lower));
  }, [rows, query]);
  const pageRows = filtered.slice(page * pageSize, page * pageSize + pageSize);

  return (
    <section className="table-panel">
      <div className="table-tools">
        <label>
          <Search size={16} />
          <input
            placeholder="Search"
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
              setPage(0);
            }}
          />
        </label>
        <span>{filtered.length} rows</span>
      </div>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>{columns.map((column) => <th key={column.key}>{column.label}</th>)}</tr>
          </thead>
          <tbody>
            {pageRows.map((row) => (
              <tr key={row.id}>
                {columns.map((column) => (
                  <td key={column.key}>
                    {column.key === "status" ? (
                      <span className={statusClass(row[column.key])}>{row[column.key]}</span>
                    ) : (
                      String(row[column.key] ?? "")
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="pagination">
        <button disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button>
        <span>Page {page + 1}</span>
        <button
          disabled={(page + 1) * pageSize >= filtered.length}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </section>
  );
}

function App() {
  const [active, setActive] = useState("dashboard");
  const [dark, setDark] = useState(true);
  const [token, setToken] = useState("");
  const [data, setData] = useState({
    overview: {},
    pipelines: [],
    airflow: [],
    spark: [],
    quality: [],
    performance: {}
  });
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [overview, pipelines, airflow, spark, quality, performance] = await Promise.all([
          fetchJson("/api/v1/metrics/overview", token),
          fetchJson("/api/v1/pipeline-runs", token),
          fetchJson("/api/v1/airflow/dag-runs", token),
          fetchJson("/api/v1/spark/jobs", token),
          fetchJson("/api/v1/data-quality/checks", token),
          fetchJson("/api/v1/metrics/performance", token)
        ]);
        setData({ overview, pipelines, airflow, spark, quality, performance });
        setError("");
      } catch (err) {
        setError(String(err.message || err));
      }
    }
    load();
  }, [token]);

  const chartData = [
    { name: "Success", value: data.overview.successful_runs || 0, color: "#22c55e" },
    { name: "Failed", value: data.overview.failed_runs || 0, color: "#ef4444" }
  ];

  return (
    <main className={dark ? "app dark" : "app"}>
      <aside>
        <div className="brand"><Activity /> DataPulse</div>
        {views.map((view) => {
          const Icon = view.icon;
          return (
            <button
              className={active === view.id ? "active" : ""}
              key={view.id}
              onClick={() => setActive(view.id)}
            >
              <Icon size={18} /> {view.label}
            </button>
          );
        })}
      </aside>
      <section className="content">
        <header>
          <div>
            <h1>{views.find((view) => view.id === active)?.label}</h1>
            <p>Enterprise data observability control plane</p>
          </div>
          <button className="icon-button" onClick={() => setDark(!dark)}>
            {dark ? <Sun /> : <Moon />}
          </button>
        </header>
        {error && <div className="banner"><AlertTriangle size={16} /> {error}</div>}
        {active === "dashboard" && (
          <>
            <div className="cards">
              <Card title="Pipeline Runs" value={data.overview.total_pipeline_runs || 0} />
              <Card title="Successful Runs" value={data.overview.successful_runs || 0} tone="good" />
              <Card title="Failed Runs" value={data.overview.failed_runs || 0} tone="bad" />
              <Card title="Records Processed" value={data.overview.total_records_processed || 0} />
            </div>
            <section className="chart-grid">
              <div className="chart-panel">
                <h3>Pipeline Health</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <PieChart>
                    <Pie data={chartData} dataKey="value" outerRadius={90} label>
                      {chartData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="chart-panel">
                <h3>Operational Failures</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={[
                    { name: "SLA", value: data.overview.airflow_sla_misses || 0 },
                    { name: "Spark", value: data.overview.failed_spark_jobs || 0 },
                    { name: "DQ", value: data.overview.failed_data_quality_checks || 0 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#38bdf8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </section>
          </>
        )}
        {active === "pipelines" && <DataTable rows={data.pipelines} columns={[
          { key: "pipeline_name", label: "Pipeline" },
          { key: "pipeline_type", label: "Type" },
          { key: "status", label: "Status" },
          { key: "duration_seconds", label: "Duration" },
          { key: "records_processed", label: "Records" }
        ]} />}
        {active === "airflow" && <DataTable rows={data.airflow} columns={[
          { key: "dag_id", label: "DAG" },
          { key: "run_id", label: "Run" },
          { key: "status", label: "Status" },
          { key: "failed_tasks", label: "Failed Tasks" },
          { key: "retry_count", label: "Retries" },
          { key: "sla_miss", label: "SLA Miss" }
        ]} />}
        {active === "spark" && <DataTable rows={data.spark} columns={[
          { key: "job_name", label: "Job" },
          { key: "app_id", label: "App" },
          { key: "status", label: "Status" },
          { key: "input_records", label: "Input" },
          { key: "output_records", label: "Output" },
          { key: "partitions", label: "Partitions" }
        ]} />}
        {active === "quality" && <DataTable rows={data.quality} columns={[
          { key: "dataset_name", label: "Dataset" },
          { key: "check_name", label: "Check" },
          { key: "check_type", label: "Type" },
          { key: "status", label: "Status" },
          { key: "failed_records", label: "Failed" },
          { key: "total_records", label: "Total" }
        ]} />}
        {active === "metrics" && (
          <div className="cards">
            <Card title="API Requests" value={data.performance.request_count || 0} />
            <Card title="API Errors" value={data.performance.error_count || 0} tone="bad" />
            <Card title="Avg Duration" value={`${data.performance.average_duration_ms || 0} ms`} />
          </div>
        )}
        <Login onLogin={setToken} />
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
