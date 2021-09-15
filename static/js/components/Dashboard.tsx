import * as React from "react";
import { Strip } from "@canonical/react-components";
import { InterviewParticipation } from "./InterviewParticipation";
import { JobsDetails } from "./JobsDetails";

export const Dashboard: React.FC<any> = () => {
  return (
    <div className="l-application">
      <main className="l-main">
        <Strip>
          <h1>Hiring Dashboard</h1>
        </Strip>
        <JobsDetails />
        <InterviewParticipation />
      </main>
    </div>
  );
};
