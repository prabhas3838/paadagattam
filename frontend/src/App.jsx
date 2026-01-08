import { useState } from "react";
import RoundStatus from "./components/RoundStatus";
import SeatBox from "./components/SeatBox";
import PreferenceForm from "./components/PreferenceForm";
import RunAllocation from "./components/RunAllocation";
import AllocationResult from "./components/AllocationResult";
import CandidateRegister from "./components/CandidateRegister";
import MySeat from "./components/MySeat";

export default function App() {
  const [candidateId, setCandidateId] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-6">
        Voice-Based Admission Portal
      </h1>

      <RoundStatus roundNo={2} />

      {/* ✅ FIX HERE */}
      <RunAllocation
        roundNo={1}
        onDone={() => setRefreshKey(k => k + 1)}
      />

      <CandidateRegister onRegistered={setCandidateId} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <SeatBox />
        <PreferenceForm candidateId={candidateId} />
      </div>

      <AllocationResult
        candidateId={candidateId}
        refreshKey={refreshKey}
      />

      <MySeat
        candidateId={candidateId}
        refreshKey={refreshKey}
      />
    </div>
  );
}
