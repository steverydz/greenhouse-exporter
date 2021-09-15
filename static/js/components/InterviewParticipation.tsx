import React, { useEffect, useState } from "react";
import { MainTable, Strip } from "@canonical/react-components";

export const InterviewParticipation: React.FC<any> = () => {
  const [interviews, setInterviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getInterviews = async () => {
      try {
        const response = await fetch("/api/interviews");
        if (response.status === 200) {
          setInterviews(await response.json());
        }
      } catch (error) {
        console.error("Error fetching endpoint /api/interviews: ", error);
      } finally {
        setIsLoading(false);
      }
    };
    getInterviews();
  }, []);

  return (
    <Strip type="light" shallow={true}>
      <h2>Interview participation</h2>
      <MainTable
        headers={[
          { content: "Applicant", sortKey: "applicant" },
          { content: "Date", sortKey: "date" },
          { content: "Stage", sortKey: "stage" },
          { content: "Status", sortKey: "status" },
        ]}
        rows={interviews.map(
          ({ applicant, date, current_stage, application_status }) => {
            return {
              columns: [
                { content: applicant },
                { content: date },
                { content: current_stage },
                { content: application_status },
              ],
              sortData: {
                applicant: applicant,
                date: new Date(date),
                stage: current_stage,
                status: application_status,
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
