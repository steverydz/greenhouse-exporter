import React, { useEffect, useState } from "react";
import { MainTable, Strip } from "@canonical/react-components";

export const JobsDetails: React.FC<any> = () => {
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getJobs = async () => {
      try {
        const response = await fetch("/api/jobs");
        if (response.status === 200) {
          setJobs(await response.json());
        }
      } catch (error) {
        console.error("Error fetching endpoint /api/jobs: ", error);
      } finally {
        setIsLoading(false);
      }
    };
    getJobs();
  }, []);

  return (
    <Strip type="light" shallow={true}>
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
        paginate={10}
        emptyStateMsg={
          isLoading ? (
            <i className="p-icon--spinner u-animation--spin"></i>
          ) : (
            <i>No data could be fetched</i>
          )
        }
      />
    </Strip>
  );
};
