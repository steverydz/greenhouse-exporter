import * as React from "react";
import { Strip } from "@canonical/react-components";
import { InterviewParticipation } from "./InterviewParticipation";
import { JobsDetails } from "./JobsDetails";
import { Workload } from "./Workload";

export const Dashboard: React.FC<any> = () => {
  return (
    <div className="l-application">
      <main className="l-main">
        <Strip shallow={true}>
          <h1>Hiring Dashboard</h1>
        </Strip>
        <JobsDetails />
        <InterviewParticipation />
        <Workload />
      </main>
    </div>
  );
};
