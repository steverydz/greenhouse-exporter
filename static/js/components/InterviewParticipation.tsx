import React, { useEffect, useState } from "react";
import { MainTable } from "@canonical/react-components";

export const InterviewParticipation: React.FC<{}> = () => {
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const getInterviews = async () => {
      const response = await fetch("/api/get-jobs.json");
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
            { content: "Status" },
          ]}
          rows={interviews.map(({ applicant, date, status }) => {
            return {
              columns: [
                { content: applicant },
                { content: date },
                { content: status },
              ],
            };
          })}
        />
      </div>
    </section>
  );
};
