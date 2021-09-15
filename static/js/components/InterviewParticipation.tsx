import React, { useEffect, useState } from "react";
import { MainTable, Strip } from "@canonical/react-components";

export const InterviewParticipation: React.FC<any> = () => {
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const getInterviews = async () => {
      const response = await fetch("/api/interviews");
      setInterviews(await response.json());
    };
    getInterviews();
  }, []);

  return (
    <Strip type="light">
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
        emptyStateMsg={<i className="p-icon--spinner u-animation--spin"></i>}
      />
    </Strip>
  );
};
