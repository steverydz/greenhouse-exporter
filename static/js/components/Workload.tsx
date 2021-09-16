import React, { useEffect, useState } from "react";
import { MainTable, Strip } from "@canonical/react-components";

export const Workload: React.FC<any> = () => {
  const [workload, setWorkload] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getWorkload = async () => {
      try {
        const response = await fetch("/api/workload");
        if (response.status === 200) {
          setWorkload(await response.json());
        }
      } catch (error) {
        console.error("Error fetching endpoint /api/workload: ", error);
      } finally {
        setIsLoading(false);
      }
    };
    getWorkload();
  }, []);

  return (
    <Strip type="light" shallow={true}>
      <h2>Workload</h2>
      <MainTable
        headers={[
          { content: "Interviewer", sortKey: "interviewer" },
          { content: "Date", sortKey: "date" },
          { content: "Stage", sortKey: "stage" },
          { content: "Estimated duration", sortKey: "estimated_duration" },
        ]}
        rows={workload.map(
          ({ interviewer, stage, date, estimated_duration }) => {
            return {
              columns: [
                { content: interviewer },
                { content: date },
                { content: stage },
                { content: estimated_duration },
              ],
              sortData: {
                interviewer: interviewer,
                date: date,
                stage: stage,
                estimated_duration: estimated_duration,
              },
            };
          }
        )}
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
