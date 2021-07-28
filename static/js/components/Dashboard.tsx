import * as React from "react";
import { InterviewParticipation } from "./InterviewParticipation";
import { JobsDetails } from "./JobsDetails";

export const Dashboard: React.FC<{}> = () => {
  return (
    <div className="l-application">
      <main className="l-main">
        <section className="p-strip">
          <div className="row">
            <h1>Hiring Dashboard</h1>
          </div>
        </section>
        <JobsDetails />
        <InterviewParticipation />
      </main>
    </div>
  );
};
