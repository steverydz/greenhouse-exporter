import React, { useEffect, useState } from "react";
import { MainTable, Strip } from "@canonical/react-components";

export const JobsDetails: React.FC<any> = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const getJobs = async () => {
      const response = await fetch("/api/jobs");
      setJobs(await response.json());
    };
    getJobs();
  }, []);

  return (
    <Strip type="light">
      <h2>Jobs details</h2>
      <MainTable
        headers={[
          { content: "Job", sortKey: "job" },
          { content: "Total applications", sortKey: "applications" },
        ]}
        rows={jobs.map(({ job, applications }) => {
          return {
            columns: [{ content: job }, { content: applications }],
            sortData: { job: job, applications: applications },
          };
        })}
        sortable
        emptyStateMsg={<i className="p-icon--spinner u-animation--spin"></i>}
      />
    </Strip>
  );
};
