import React, { useEffect, useState } from "react";
import { MainTable } from "@canonical/react-components";

export const InterviewParticipation: React.FC<{}> = () => {
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const getInterviews = async () => {
      const response = await fetch("/api/interviews");
      setInterviews(await response.json());
    };
    getInterviews();
  });

  return (
    <section className="p-strip--light">
      <div className="row">
        <h2>Interview participation</h2>
        <MainTable
          headers={[
            { content: "Applicant" },
            { content: "Date" },
            { content: "Stage" },
            { content: "Status" },
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
              };
            }
          )}
        />
      </div>
    </section>
  );
};
