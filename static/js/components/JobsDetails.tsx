import React, { useEffect, useState } from "react";
import { MainTable } from "@canonical/react-components";

export const JobsDetails: React.FC<{}> = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const getJobs = async () => {
      const response = await fetch("/api/jobs");
      setJobs(await response.json());
    };
    getJobs();
  });

  return (
    <section className="p-strip--light">
      <div className="row">
        <h2>Jobs details</h2>
        <MainTable
          headers={[{ content: "Job" }, { content: "Total applications" }]}
          rows={jobs.map(({ job, applications }) => {
            return { columns: [{ content: job }, { content: applications }] };
          })}
        />
      </div>
    </section>
  );
};
