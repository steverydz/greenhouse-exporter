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
          { content: "Employee", sortKey: "employee" },
          { content: "Type", sortKey: "type" },
          { content: "Date", sortKey: "date" },
          { content: "Estimated duration", sortKey: "estimated_duration" },
          { content: "Status", sortKey: "status" },
        ]}
        rows={workload.map(
          ({ employee, type, date, estimated_duration, status }) => {
            return {
              columns: [
                { content: employee },
                { content: type },
                { content: date },
                { content: estimated_duration },
                { content: status },
              ],
              sortData: {
                employee: employee,
                type: type,
                date: new Date(date),
                estimated_duration: estimated_duration,
                status: status,
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
